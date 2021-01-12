#pragma once
// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include the main libnx system header, for Switch development
#include <switch.h>

// Yes, I know this is from main, but I don't want to make a "main.hpp" just for this
int printToFile(const char* myString);

class FakeController {
public:
    HiddbgHdlsHandle controllerHandle = {0};
    HiddbgHdlsDeviceInfo controllerDevice = {0};
    HiddbgHdlsState controllerState = {0};
    int initialize(u16);
    int deInitialize();
    bool isInitialized = false;
    
};