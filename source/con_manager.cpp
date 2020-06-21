#include "con_manager.hpp"
#include "udp_manager.hpp"
#include <mutex>

int FakeController::initialize()
{
    if (isInitialized == true) return 0;
    Result myResult;
    //printToFile("Controller initializing...");

    // Set the controller type to Pro-Controller, and set the npadInterfaceType.
    controllerDevice.deviceType = HidDeviceType_FullKey3; // FullKey3 for Pro Controller, JoyLeft4 for left joy con
    controllerDevice.npadInterfaceType = NpadInterfaceType_Bluetooth;
    // Set the controller colors. The grip colors are for Pro-Controller on [9.0.0+].
    controllerDevice.singleColorBody = RGBA8_MAXALPHA(255,153,204);
    controllerDevice.singleColorButtons = RGBA8_MAXALPHA(0,0,0);
    controllerDevice.colorLeftGrip = RGBA8_MAXALPHA(255,0,127);
    controllerDevice.colorRightGrip = RGBA8_MAXALPHA(255,0,127);

    // Setup example controller state.
    controllerState.batteryCharge = 4; // Set battery charge to full.
    controllerState.joysticks[JOYSTICK_LEFT].dx = 0x0;
    controllerState.joysticks[JOYSTICK_LEFT].dy = -0x0;
    controllerState.joysticks[JOYSTICK_RIGHT].dx = 0x0;
    controllerState.joysticks[JOYSTICK_RIGHT].dy = -0x0;
    
    myResult = hiddbgAttachHdlsVirtualDevice(&controllerHandle, &controllerDevice);
    if (R_FAILED(myResult)) {
        //printToFile("Failed connecting controller... fuck");
        return -1;
    }

    //printToFile("Controller initialized!");
    isInitialized = true;
    return 0;
}

int FakeController::deInitialize()
{
    if (isInitialized == false) return 0;
    Result myResult;
    
    myResult = hiddbgDetachHdlsVirtualDevice(controllerHandle);
    if (R_FAILED(myResult)) {
        return -1;
    }

    isInitialized = false;
    return 0;
}

FakeController fakeControllerList [4];
s16 controllersConnected = 0;
u64 last_time_recorded;

void apply_fake_con_state(struct input_message message)
{
    u64 tmp_time_recorded = svcGetSystemTick();
    if (tmp_time_recorded - last_time_recorded > (19200000 / 10) && controllersConnected > 0)
    {
        // Detect Sleep Mode
        svcSleepThread(5e+8L);
        
        // Since we woke up from Sleep Mode, we'll disconnect each controller
        for (int i = 0; i < controllersConnected; i++)
        {
            fakeControllerList[i].deInitialize();
        }
        controllersConnected = 0;

        tmp_time_recorded = svcGetSystemTick();
    }
    last_time_recorded = tmp_time_recorded;

    // Check if the magic is correct
    if(message.magic != INPUT_MSG_MAGIC)
        return;
    
    // If there is no controller connected, we have to initialize one
    if (fakeControllerList[0].isInitialized == false)
    {
        fakeControllerList[0].initialize();
        controllersConnected++;
    }

    // Set the controller sticks and joystick according to what the network told us
    fakeControllerList[0].controllerState.buttons = message.keys;
    fakeControllerList[0].controllerState.joysticks[0].dx = message.joy_l_x;
    fakeControllerList[0].controllerState.joysticks[0].dy = message.joy_l_y;
    fakeControllerList[0].controllerState.joysticks[1].dx = message.joy_r_x;
    fakeControllerList[0].controllerState.joysticks[1].dy = message.joy_r_y;
    hiddbgSetHdlsState(fakeControllerList[0].controllerHandle, &fakeControllerList[0].controllerState);
    
    return;
}

static Mutex pkgMutex;
static struct input_message fakeConsState;

void networkThread(void* _)
{
    struct input_message temporal_pkg;
    while (true)
    {
        int poll_res = poll_udp_input(&temporal_pkg);
        mutexLock(&pkgMutex);

        if (poll_res == 0)
        {
            fakeConsState = temporal_pkg;
            apply_fake_con_state(fakeConsState);
        }
        else
        {
            fakeConsState.magic = 0;
            svcSleepThread(1e+7l);
        }
        mutexUnlock(&pkgMutex);

        svcSleepThread(-1);
    }
}