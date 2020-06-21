// Include the most common headers from the C standard library
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Include the main libnx system header, for Switch development
#include <switch.h>

// Other stuff
#include <malloc.h>
#include "con_manager.hpp"
#include "udp_manager.hpp"
#include <cstdlib>
#include <cstdint>
#include <cstring>
#include <optional>
#include <mutex>

static const SocketInitConfig sockInitConf = {
    .bsdsockets_version = 1,

    .tcp_tx_buf_size        = 0x200,
    .tcp_rx_buf_size        = 0x400,
    .tcp_tx_buf_max_size    = 0x400,
    .tcp_rx_buf_max_size    = 0x800,
    // We're not using tcp anyways

    .udp_tx_buf_size = 0x2600,
    .udp_rx_buf_size = 0xA700,

    .sb_efficiency = 2,

    .num_bsd_sessions = 3,
    .bsd_service_type = BsdServiceType_User
};

extern "C" {
    // Sysmodules should not use applet*.
    u32 __nx_applet_type = AppletType_None;
    // Sysmodules will normally only want to use one FS session.
    //u32 __nx_fs_num_sessions = 1;


    // Adjust size as needed.
    #define INNER_HEAP_SIZE 0x80000
    size_t nx_inner_heap_size = INNER_HEAP_SIZE;
    char   nx_inner_heap[INNER_HEAP_SIZE];

    void __libnx_init_time(void);
    void __libnx_initheap(void);
    void __appInit(void);
    void __appExit(void);


    void __libnx_initheap(void)
    {
        void*  addr = nx_inner_heap;
        size_t size = nx_inner_heap_size;

        // Newlib
        extern char* fake_heap_start;
        extern char* fake_heap_end;

        fake_heap_start = (char*)addr;
        fake_heap_end   = (char*)addr + size;
    }

    // Init/exit services, update as needed.
    void __attribute__((weak)) __appInit(void)
    {
        Result rc;
        // Initialize default services.
        rc = smInitialize();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_SM));

        if (hosversionGet() == 0) {
            rc = setsysInitialize();
            if (R_SUCCEEDED(rc)) {
                SetSysFirmwareVersion fw;
                rc = setsysGetFirmwareVersion(&fw);
                if (R_SUCCEEDED(rc))
                    hosversionSet(MAKEHOSVERSION(fw.major, fw.minor, fw.micro));
                setsysExit();
            }
        }

        // Enable this if you want to use HID.
        rc = hidInitialize();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_HID));

        rc = hiddbgInitialize();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_HID));

        //Enable this if you want to use time.
        rc = timeInitialize();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_Time));

        __libnx_init_time();

        rc = fsInitialize();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_FS));

        rc = fsdevMountSdmc();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_FS));

        rc = hiddbgAttachHdlsWorkBuffer();
        if (R_FAILED(rc))
            fatalThrow(MAKERESULT(Module_Libnx, LibnxError_InitFail_HID));

        rc = pmdmntInitialize();
        if (R_FAILED(rc)) 
            fatalThrow(rc);

        rc = ldrDmntInitialize();
        if (R_FAILED(rc)) 
            fatalThrow(rc);

        rc = pminfoInitialize();
        if (R_FAILED(rc)) 
            fatalThrow(rc);

        rc = socketInitialize(&sockInitConf);
        if (R_FAILED(rc))
            fatalThrow(rc);

        rc = capsscInitialize();
        if (R_FAILED(rc))
            fatalThrow(rc);
        
    }

    void __attribute__((weak)) userAppExit(void);

    void __attribute__((weak)) __appExit(void)
    {
        // Cleanup default services.
        fsdevUnmountAll();
        fsExit();
        timeExit();//Enable this if you want to use time.
        hidExit();// Enable this if you want to use HID.
        smExit();
        socketExit();
    }
}

int printToFile(const char* myString)
{
    FILE *log = fopen("/hidplus/log.txt", "w+a");
    if (log != nullptr) {
            fprintf(log, myString);
            fclose(log);
    }
    return 0;
}

// Main program entrypoint
u64 mainLoopSleepTime = 50;
static Thread network_thread;
int main(int argc, char* argv[])
{
    // Initialization code can go here.

    // Your code / main loop goes here.
    // If you need threads, you can use threadCreate etc.

    printToFile("READY!");
    FakeController testController;
    
    threadCreate(&network_thread, networkThread, NULL, NULL, 0x1000, 0x30, 3);
    threadStart(&network_thread);
    
    while (appletMainLoop()) // Main loop
    {

        hidScanInput();

        u64 kDown = hidKeysDown(CONTROLLER_P1_AUTO);

        /*if (kDown & KEY_PLUS)
        {
            // Start the controller
            testController.initialize();
            // Press A
            testController.controllerState.buttons = 1;
            hiddbgSetHdlsState(testController.controllerHandle, &testController.controllerState);
            // Unpress A
            svcSleepThread(1000 * 1e+6L);
            testController.controllerState.buttons = 0;
            hiddbgSetHdlsState(testController.controllerHandle, &testController.controllerState);
        }*/

        svcSleepThread(mainLoopSleepTime * 1e+6L);

    }

    // Deinitialization and resources clean up code can go here.
    return 0;
}
