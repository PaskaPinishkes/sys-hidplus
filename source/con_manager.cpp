#include "con_manager.hpp"

int FakeController::initialize()
{
    if (isInitialized == true) return 0;
    Result myResult;
    printToFile("Controller initializing...");
        
    
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
        printToFile("Failed connecting controller... fuck");
        return -1;
    }

    printToFile("Controller initialized!");
    isInitialized = true;
    return 0;
}