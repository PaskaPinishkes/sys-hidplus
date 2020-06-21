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

FakeController testController2;
void apply_fake_con_state(struct input_message message)
{
    if(message.magic != INPUT_MSG_MAGIC)
        return;
    
    if (testController2.isInitialized == false)
    {
        testController2.initialize();
    }

    testController2.controllerState.buttons = message.keys;
    testController2.controllerState.joysticks[0].dx = message.joy_l_x;
    testController2.controllerState.joysticks[0].dy = message.joy_l_y;
    testController2.controllerState.joysticks[1].dx = message.joy_r_x;
    testController2.controllerState.joysticks[1].dy = message.joy_r_y;
    hiddbgSetHdlsState(testController2.controllerHandle, &testController2.controllerState);
    
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