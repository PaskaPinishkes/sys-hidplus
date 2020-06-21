// Most of the UDP code comes from hid-mitm: https://github.com/jakibaki/hid-mitm

#include <switch.h>
#define INPUT_MSG_MAGIC 0x3276

class input_message
{
public:
    u16 magic;
    u64 keys;
    s32 joy_l_x;
    s32 joy_l_r;
    s32 joy_r_x;
    s32 joy_r_r;
};

int poll_udp_input(input_message* buf);