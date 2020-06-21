// Most of the UDP code comes from hid-mitm: https://github.com/jakibaki/hid-mitm

extern "C" {
    #include <switch.h>
    #define INPUT_MSG_MAGIC 0x3275

    struct __attribute__((__packed__)) input_message
    {
    public:
        u16 magic;
        u64 keys;
        s32 joy_l_x;
        s32 joy_l_y;
        s32 joy_r_x;
        s32 joy_r_y;
    };

    int poll_udp_input(input_message* buf);
    void networkThread(void* _);
}