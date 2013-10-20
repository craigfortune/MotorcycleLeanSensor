#!/usr/bin/python

# Python Standard Library Imports
from time import sleep
from math import atan, atan2, sqrt

# External Imports
pass

# Custom Imports
from pycomms import PyComms

class MPU6050:
    # Register map based on Jeff Rowberg <jeff@rowberg.net> source code at
    # https://github.com/jrowberg/i2cdevlib/blob/master/Arduino/MPU6050/MPU6050.h
    
    MPU6050_ADDRESS_AD0_LOW       = 0x68 # address pin low (GND), default for InvenSense evaluation board
    MPU6050_ADDRESS_AD0_HIGH      = 0x69 # address pin high (VCC)
    MPU6050_DEFAULT_ADDRESS       = MPU6050_ADDRESS_AD0_LOW

    MPU6050_RA_XG_OFFS_TC         = 0x00 # [7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_YG_OFFS_TC         = 0x01 # [7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_ZG_OFFS_TC         = 0x02 # [7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_X_FINE_GAIN        = 0x03 # [7:0] X_FINE_GAIN
    MPU6050_RA_Y_FINE_GAIN        = 0x04 # [7:0] Y_FINE_GAIN
    MPU6050_RA_Z_FINE_GAIN        = 0x05 # [7:0] Z_FINE_GAIN
    MPU6050_RA_XA_OFFS_H          = 0x06 # [15:0] XA_OFFS
    MPU6050_RA_XA_OFFS_L_TC       = 0x07
    MPU6050_RA_YA_OFFS_H          = 0x08 # [15:0] YA_OFFS
    MPU6050_RA_YA_OFFS_L_TC       = 0x09
    MPU6050_RA_ZA_OFFS_H          = 0x0A # [15:0] ZA_OFFS
    MPU6050_RA_ZA_OFFS_L_TC       = 0x0B
    MPU6050_RA_XG_OFFS_USRH       = 0x13 # [15:0] XG_OFFS_USR
    MPU6050_RA_XG_OFFS_USRL       = 0x14
    MPU6050_RA_YG_OFFS_USRH       = 0x15 # [15:0] YG_OFFS_USR
    MPU6050_RA_YG_OFFS_USRL       = 0x16
    MPU6050_RA_ZG_OFFS_USRH       = 0x17 # [15:0] ZG_OFFS_USR
    MPU6050_RA_ZG_OFFS_USRL       = 0x18
    MPU6050_RA_SMPLRT_DIV         = 0x19
    MPU6050_RA_CONFIG             = 0x1A
    MPU6050_RA_GYRO_CONFIG        = 0x1B
    MPU6050_RA_ACCEL_CONFIG       = 0x1C
    MPU6050_RA_FF_THR             = 0x1D
    MPU6050_RA_FF_DUR             = 0x1E
    MPU6050_RA_MOT_THR            = 0x1F
    MPU6050_RA_MOT_DUR            = 0x20
    MPU6050_RA_ZRMOT_THR          = 0x21
    MPU6050_RA_ZRMOT_DUR          = 0x22
    MPU6050_RA_FIFO_EN            = 0x23
    MPU6050_RA_I2C_MST_CTRL       = 0x24
    MPU6050_RA_I2C_SLV0_ADDR      = 0x25
    MPU6050_RA_I2C_SLV0_REG       = 0x26
    MPU6050_RA_I2C_SLV0_CTRL      = 0x27
    MPU6050_RA_I2C_SLV1_ADDR      = 0x28
    MPU6050_RA_I2C_SLV1_REG       = 0x29
    MPU6050_RA_I2C_SLV1_CTRL      = 0x2A
    MPU6050_RA_I2C_SLV2_ADDR      = 0x2B
    MPU6050_RA_I2C_SLV2_REG       = 0x2C
    MPU6050_RA_I2C_SLV2_CTRL      = 0x2D
    MPU6050_RA_I2C_SLV3_ADDR      = 0x2E
    MPU6050_RA_I2C_SLV3_REG       = 0x2F
    MPU6050_RA_I2C_SLV3_CTRL      = 0x30
    MPU6050_RA_I2C_SLV4_ADDR      = 0x31
    MPU6050_RA_I2C_SLV4_REG       = 0x32
    MPU6050_RA_I2C_SLV4_DO        = 0x33
    MPU6050_RA_I2C_SLV4_CTRL      = 0x34
    MPU6050_RA_I2C_SLV4_DI        = 0x35
    MPU6050_RA_I2C_MST_STATUS     = 0x36
    MPU6050_RA_INT_PIN_CFG        = 0x37
    MPU6050_RA_INT_ENABLE         = 0x38
    MPU6050_RA_DMP_INT_STATUS     = 0x39
    MPU6050_RA_INT_STATUS         = 0x3A
    MPU6050_RA_ACCEL_XOUT_H       = 0x3B
    MPU6050_RA_ACCEL_XOUT_L       = 0x3C
    MPU6050_RA_ACCEL_YOUT_H       = 0x3D
    MPU6050_RA_ACCEL_YOUT_L       = 0x3E
    MPU6050_RA_ACCEL_ZOUT_H       = 0x3F
    MPU6050_RA_ACCEL_ZOUT_L       = 0x40
    MPU6050_RA_TEMP_OUT_H         = 0x41
    MPU6050_RA_TEMP_OUT_L         = 0x42
    MPU6050_RA_GYRO_XOUT_H        = 0x43
    MPU6050_RA_GYRO_XOUT_L        = 0x44
    MPU6050_RA_GYRO_YOUT_H        = 0x45
    MPU6050_RA_GYRO_YOUT_L        = 0x46
    MPU6050_RA_GYRO_ZOUT_H        = 0x47
    MPU6050_RA_GYRO_ZOUT_L        = 0x48
    MPU6050_RA_EXT_SENS_DATA_00   = 0x49
    MPU6050_RA_EXT_SENS_DATA_01   = 0x4A
    MPU6050_RA_EXT_SENS_DATA_02   = 0x4B
    MPU6050_RA_EXT_SENS_DATA_03   = 0x4C
    MPU6050_RA_EXT_SENS_DATA_04   = 0x4D
    MPU6050_RA_EXT_SENS_DATA_05   = 0x4E
    MPU6050_RA_EXT_SENS_DATA_06   = 0x4F
    MPU6050_RA_EXT_SENS_DATA_07   = 0x50
    MPU6050_RA_EXT_SENS_DATA_08   = 0x51
    MPU6050_RA_EXT_SENS_DATA_09   = 0x52
    MPU6050_RA_EXT_SENS_DATA_10   = 0x53
    MPU6050_RA_EXT_SENS_DATA_11   = 0x54
    MPU6050_RA_EXT_SENS_DATA_12   = 0x55
    MPU6050_RA_EXT_SENS_DATA_13   = 0x56
    MPU6050_RA_EXT_SENS_DATA_14   = 0x57
    MPU6050_RA_EXT_SENS_DATA_15   = 0x58
    MPU6050_RA_EXT_SENS_DATA_16   = 0x59
    MPU6050_RA_EXT_SENS_DATA_17   = 0x5A
    MPU6050_RA_EXT_SENS_DATA_18   = 0x5B
    MPU6050_RA_EXT_SENS_DATA_19   = 0x5C
    MPU6050_RA_EXT_SENS_DATA_20   = 0x5D
    MPU6050_RA_EXT_SENS_DATA_21   = 0x5E
    MPU6050_RA_EXT_SENS_DATA_22   = 0x5F
    MPU6050_RA_EXT_SENS_DATA_23   = 0x60
    MPU6050_RA_MOT_DETECT_STATUS  = 0x61
    MPU6050_RA_I2C_SLV0_DO        = 0x63
    MPU6050_RA_I2C_SLV1_DO        = 0x64
    MPU6050_RA_I2C_SLV2_DO        = 0x65
    MPU6050_RA_I2C_SLV3_DO        = 0x66
    MPU6050_RA_I2C_MST_DELAY_CTRL = 0x67
    MPU6050_RA_SIGNAL_PATH_RESET  = 0x68
    MPU6050_RA_MOT_DETECT_CTRL    = 0x69
    MPU6050_RA_USER_CTRL          = 0x6A
    MPU6050_RA_PWR_MGMT_1         = 0x6B
    MPU6050_RA_PWR_MGMT_2         = 0x6C
    MPU6050_RA_BANK_SEL           = 0x6D
    MPU6050_RA_MEM_START_ADDR     = 0x6E
    MPU6050_RA_MEM_R_W            = 0x6F
    MPU6050_RA_DMP_CFG_1          = 0x70
    MPU6050_RA_DMP_CFG_2          = 0x71
    MPU6050_RA_FIFO_COUNTH        = 0x72
    MPU6050_RA_FIFO_COUNTL        = 0x73
    MPU6050_RA_FIFO_R_W           = 0x74
    MPU6050_RA_WHO_AM_I           = 0x75  

    MPU6050_TC_PWR_MODE_BIT    = 7
    MPU6050_TC_OFFSET_BIT      = 6
    MPU6050_TC_OFFSET_LENGTH   = 6
    MPU6050_TC_OTP_BNK_VLD_BIT = 0

    MPU6050_VDDIO_LEVEL_VLOGIC  = 0
    MPU6050_VDDIO_LEVEL_VDD     = 1    

    MPU6050_CFG_EXT_SYNC_SET_BIT    = 5
    MPU6050_CFG_EXT_SYNC_SET_LENGTH = 3
    MPU6050_CFG_DLPF_CFG_BIT    = 2
    MPU6050_CFG_DLPF_CFG_LENGTH = 3

    MPU6050_EXT_SYNC_DISABLED      = 0x0
    MPU6050_EXT_SYNC_TEMP_OUT_L    = 0x1
    MPU6050_EXT_SYNC_GYRO_XOUT_L   = 0x2
    MPU6050_EXT_SYNC_GYRO_YOUT_L   = 0x3
    MPU6050_EXT_SYNC_GYRO_ZOUT_L   = 0x4
    MPU6050_EXT_SYNC_ACCEL_XOUT_L  = 0x5
    MPU6050_EXT_SYNC_ACCEL_YOUT_L  = 0x6
    MPU6050_EXT_SYNC_ACCEL_ZOUT_L  = 0x7

    MPU6050_DLPF_BW_256        = 0x00
    MPU6050_DLPF_BW_188        = 0x01
    MPU6050_DLPF_BW_98         = 0x02
    MPU6050_DLPF_BW_42         = 0x03
    MPU6050_DLPF_BW_20         = 0x04
    MPU6050_DLPF_BW_10         = 0x05
    MPU6050_DLPF_BW_5          = 0x06

    MPU6050_GCONFIG_FS_SEL_BIT     = 4
    MPU6050_GCONFIG_FS_SEL_LENGTH  = 2

    MPU6050_GYRO_FS_250        = 0x00
    MPU6050_GYRO_FS_500        = 0x01
    MPU6050_GYRO_FS_1000       = 0x02
    MPU6050_GYRO_FS_2000       = 0x03

    MPU6050_ACONFIG_XA_ST_BIT         =  7
    MPU6050_ACONFIG_YA_ST_BIT         =  6
    MPU6050_ACONFIG_ZA_ST_BIT         =  5
    MPU6050_ACONFIG_AFS_SEL_BIT       =  4
    MPU6050_ACONFIG_AFS_SEL_LENGTH    =  2
    MPU6050_ACONFIG_ACCEL_HPF_BIT     =  2
    MPU6050_ACONFIG_ACCEL_HPF_LENGTH  =  3

    MPU6050_ACCEL_FS_2         = 0x00
    MPU6050_ACCEL_FS_4         = 0x01
    MPU6050_ACCEL_FS_8         = 0x02
    MPU6050_ACCEL_FS_16        = 0x03

    MPU6050_DHPF_RESET         = 0x00
    MPU6050_DHPF_5             = 0x01
    MPU6050_DHPF_2P5           = 0x02
    MPU6050_DHPF_1P25          = 0x03
    MPU6050_DHPF_0P63          = 0x04
    MPU6050_DHPF_HOLD          = 0x07

    MPU6050_TEMP_FIFO_EN_BIT   = 7
    MPU6050_XG_FIFO_EN_BIT     = 6
    MPU6050_YG_FIFO_EN_BIT     = 5
    MPU6050_ZG_FIFO_EN_BIT     = 4
    MPU6050_ACCEL_FIFO_EN_BIT  = 3
    MPU6050_SLV2_FIFO_EN_BIT   = 2
    MPU6050_SLV1_FIFO_EN_BIT   = 1
    MPU6050_SLV0_FIFO_EN_BIT   = 0

    MPU6050_MULT_MST_EN_BIT    = 7
    MPU6050_WAIT_FOR_ES_BIT    = 6
    MPU6050_SLV_3_FIFO_EN_BIT  = 5
    MPU6050_I2C_MST_P_NSR_BIT  = 4
    MPU6050_I2C_MST_CLK_BIT    = 3
    MPU6050_I2C_MST_CLK_LENGTH = 4

    MPU6050_CLOCK_DIV_348      = 0x0
    MPU6050_CLOCK_DIV_333      = 0x1
    MPU6050_CLOCK_DIV_320      = 0x2
    MPU6050_CLOCK_DIV_308      = 0x3
    MPU6050_CLOCK_DIV_296      = 0x4
    MPU6050_CLOCK_DIV_286      = 0x5
    MPU6050_CLOCK_DIV_276      = 0x6
    MPU6050_CLOCK_DIV_267      = 0x7
    MPU6050_CLOCK_DIV_258      = 0x8
    MPU6050_CLOCK_DIV_500      = 0x9
    MPU6050_CLOCK_DIV_471      = 0xA
    MPU6050_CLOCK_DIV_444      = 0xB
    MPU6050_CLOCK_DIV_421      = 0xC
    MPU6050_CLOCK_DIV_400      = 0xD
    MPU6050_CLOCK_DIV_381      = 0xE
    MPU6050_CLOCK_DIV_364      = 0xF

    MPU6050_I2C_SLV_RW_BIT     = 7
    MPU6050_I2C_SLV_ADDR_BIT   = 6
    MPU6050_I2C_SLV_ADDR_LENGTH = 7
    MPU6050_I2C_SLV_EN_BIT      = 7
    MPU6050_I2C_SLV_BYTE_SW_BIT = 6
    MPU6050_I2C_SLV_REG_DIS_BIT = 5
    MPU6050_I2C_SLV_GRP_BIT     = 4
    MPU6050_I2C_SLV_LEN_BIT     = 3
    MPU6050_I2C_SLV_LEN_LENGTH  = 4

    MPU6050_I2C_SLV4_RW_BIT        = 7
    MPU6050_I2C_SLV4_ADDR_BIT      = 6
    MPU6050_I2C_SLV4_ADDR_LENGTH   = 7
    MPU6050_I2C_SLV4_EN_BIT        = 7
    MPU6050_I2C_SLV4_INT_EN_BIT    = 6
    MPU6050_I2C_SLV4_REG_DIS_BIT   = 5
    MPU6050_I2C_SLV4_MST_DLY_BIT   = 4
    MPU6050_I2C_SLV4_MST_DLY_LENGTH = 5

    MPU6050_MST_PASS_THROUGH_BIT   = 7
    MPU6050_MST_I2C_SLV4_DONE_BIT  = 6
    MPU6050_MST_I2C_LOST_ARB_BIT   = 5
    MPU6050_MST_I2C_SLV4_NACK_BIT  = 4
    MPU6050_MST_I2C_SLV3_NACK_BIT  = 3
    MPU6050_MST_I2C_SLV2_NACK_BIT  = 2
    MPU6050_MST_I2C_SLV1_NACK_BIT  = 1
    MPU6050_MST_I2C_SLV0_NACK_BIT  = 0

    MPU6050_INTCFG_INT_LEVEL_BIT       = 7
    MPU6050_INTCFG_INT_OPEN_BIT        = 6
    MPU6050_INTCFG_LATCH_INT_EN_BIT    = 5
    MPU6050_INTCFG_INT_RD_CLEAR_BIT    = 4
    MPU6050_INTCFG_FSYNC_INT_LEVEL_BIT = 3
    MPU6050_INTCFG_FSYNC_INT_EN_BIT    = 2
    MPU6050_INTCFG_I2C_BYPASS_EN_BIT   = 1
    MPU6050_INTCFG_CLKOUT_EN_BIT       = 0

    MPU6050_INTMODE_ACTIVEHIGH = 0x00
    MPU6050_INTMODE_ACTIVELOW  = 0x01

    MPU6050_INTDRV_PUSHPULL    = 0x00
    MPU6050_INTDRV_OPENDRAIN   = 0x01

    MPU6050_INTLATCH_50USPULSE = 0x00
    MPU6050_INTLATCH_WAITCLEAR = 0x01

    MPU6050_INTCLEAR_STATUSREAD = 0x00
    MPU6050_INTCLEAR_ANYREAD    = 0x01

    MPU6050_INTERRUPT_FF_BIT           = 7
    MPU6050_INTERRUPT_MOT_BIT          = 6
    MPU6050_INTERRUPT_ZMOT_BIT         = 5
    MPU6050_INTERRUPT_FIFO_OFLOW_BIT   = 4
    MPU6050_INTERRUPT_I2C_MST_INT_BIT  = 3
    MPU6050_INTERRUPT_PLL_RDY_INT_BIT  = 2
    MPU6050_INTERRUPT_DMP_INT_BIT      = 1
    MPU6050_INTERRUPT_DATA_RDY_BIT     = 0

    # TODO: figure out what these actually do
    # UMPL source code is not very obivous
    MPU6050_DMPINT_5_BIT           = 5
    MPU6050_DMPINT_4_BIT           = 4
    MPU6050_DMPINT_3_BIT           = 3
    MPU6050_DMPINT_2_BIT           = 2
    MPU6050_DMPINT_1_BIT           = 1
    MPU6050_DMPINT_0_BIT           = 0

    MPU6050_MOTION_MOT_XNEG_BIT    = 7
    MPU6050_MOTION_MOT_XPOS_BIT    = 6
    MPU6050_MOTION_MOT_YNEG_BIT    = 5
    MPU6050_MOTION_MOT_YPOS_BIT    = 4
    MPU6050_MOTION_MOT_ZNEG_BIT    = 3
    MPU6050_MOTION_MOT_ZPOS_BIT    = 2
    MPU6050_MOTION_MOT_ZRMOT_BIT   = 0

    MPU6050_DELAYCTRL_DELAY_ES_SHADOW_BIT  = 7
    MPU6050_DELAYCTRL_I2C_SLV4_DLY_EN_BIT  = 4
    MPU6050_DELAYCTRL_I2C_SLV3_DLY_EN_BIT  = 3
    MPU6050_DELAYCTRL_I2C_SLV2_DLY_EN_BIT  = 2
    MPU6050_DELAYCTRL_I2C_SLV1_DLY_EN_BIT  = 1
    MPU6050_DELAYCTRL_I2C_SLV0_DLY_EN_BIT  = 0

    MPU6050_PATHRESET_GYRO_RESET_BIT   = 2
    MPU6050_PATHRESET_ACCEL_RESET_BIT  = 1
    MPU6050_PATHRESET_TEMP_RESET_BIT   = 0

    MPU6050_DETECT_ACCEL_ON_DELAY_BIT     = 5
    MPU6050_DETECT_ACCEL_ON_DELAY_LENGTH  = 2
    MPU6050_DETECT_FF_COUNT_BIT           = 3
    MPU6050_DETECT_FF_COUNT_LENGTH        = 2
    MPU6050_DETECT_MOT_COUNT_BIT          = 1
    MPU6050_DETECT_MOT_COUNT_LENGTH       = 2

    MPU6050_DETECT_DECREMENT_RESET = 0x0
    MPU6050_DETECT_DECREMENT_1     = 0x1
    MPU6050_DETECT_DECREMENT_2     = 0x2
    MPU6050_DETECT_DECREMENT_4     = 0x3

    MPU6050_USERCTRL_DMP_EN_BIT            = 7
    MPU6050_USERCTRL_FIFO_EN_BIT           = 6
    MPU6050_USERCTRL_I2C_MST_EN_BIT        = 5
    MPU6050_USERCTRL_I2C_IF_DIS_BIT        = 4
    MPU6050_USERCTRL_DMP_RESET_BIT         = 3
    MPU6050_USERCTRL_FIFO_RESET_BIT        = 2
    MPU6050_USERCTRL_I2C_MST_RESET_BIT     = 1
    MPU6050_USERCTRL_SIG_COND_RESET_BIT    = 0

    MPU6050_PWR1_DEVICE_RESET_BIT  = 7
    MPU6050_PWR1_SLEEP_BIT         = 6
    MPU6050_PWR1_CYCLE_BIT         = 5
    MPU6050_PWR1_TEMP_DIS_BIT      = 3
    MPU6050_PWR1_CLKSEL_BIT        = 2
    MPU6050_PWR1_CLKSEL_LENGTH     = 3

    MPU6050_CLOCK_INTERNAL        =  0x00
    MPU6050_CLOCK_PLL_XGYRO       =  0x01
    MPU6050_CLOCK_PLL_YGYRO       =  0x02
    MPU6050_CLOCK_PLL_ZGYRO       =  0x03
    MPU6050_CLOCK_PLL_EXT32K      =  0x04
    MPU6050_CLOCK_PLL_EXT19M      =  0x05
    MPU6050_CLOCK_KEEP_RESET      =  0x07

    MPU6050_PWR2_LP_WAKE_CTRL_BIT     = 7
    MPU6050_PWR2_LP_WAKE_CTRL_LENGTH  = 2
    MPU6050_PWR2_STBY_XA_BIT          = 5
    MPU6050_PWR2_STBY_YA_BIT          = 4
    MPU6050_PWR2_STBY_ZA_BIT          = 3
    MPU6050_PWR2_STBY_XG_BIT          = 2
    MPU6050_PWR2_STBY_YG_BIT          = 1
    MPU6050_PWR2_STBY_ZG_BIT          = 0

    MPU6050_WAKE_FREQ_1P25     = 0x0
    MPU6050_WAKE_FREQ_2P5      = 0x1
    MPU6050_WAKE_FREQ_5        = 0x2
    MPU6050_WAKE_FREQ_10       = 0x3

    MPU6050_BANKSEL_PRFTCH_EN_BIT      = 6
    MPU6050_BANKSEL_CFG_USER_BANK_BIT  = 5
    MPU6050_BANKSEL_MEM_SEL_BIT        = 4
    MPU6050_BANKSEL_MEM_SEL_LENGTH     = 5
 
    MPU6050_BANKSEL_PRFTCH_EN_BIT = 6
    MPU6050_BANKSEL_CFG_USER_BANK_BIT = 5
    MPU6050_BANKSEL_MEM_SEL_BIT   = 4
    MPU6050_BANKSEL_MEM_SEL_LENGTH = 5    
    
    MPU6050_WHO_AM_I_BIT          = 6
    MPU6050_WHO_AM_I_LENGTH       = 6    
    
    # DMP
    
    MPU6050_DMP_MEMORY_BANKS      = 8
    MPU6050_DMP_MEMORY_BANK_SIZE  = 256
    MPU6050_DMP_MEMORY_CHUNK_SIZE = 16
    
    MPU6050_DMP_CODE_SIZE         = 1929    # dmpMemory[]
    MPU6050_DMP_CONFIG_SIZE       = 192     # dmpConfig[]
    MPU6050_DMP_UPDATES_SIZE      = 47      # dmpUpdates[]
    # ====================================================================================================
    # | Default MotionApps v2.0 42-byte FIFO packet structure:                                           |
    # |                                                                                                  |
    # | [QUAT W][      ][QUAT X][      ][QUAT Y][      ][QUAT Z][      ][GYRO X][      ][GYRO Y][      ] |
    # |   0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  |
    # |                                                                                                  |
    # | [GYRO Z][      ][ACC X ][      ][ACC Y ][      ][ACC Z ][      ][      ]                         |
    # |  24  25  26  27  28  29  30  31  32  33  34  35  36  37  38  39  40  41                          |
    # ====================================================================================================    

    # this block of memory gets written to the MPU on start-up, and it seems
    # to be volatile memory, so it has to be done each time (it only takes ~1 second though) 
    dmpMemory = [
        # bank 0, 256 bytes
        0xFB, 0x00, 0x00, 0x3E, 0x00, 0x0B, 0x00, 0x36, 0x00, 0x01, 0x00, 0x02, 0x00, 0x03, 0x00, 0x00,
        0x00, 0x65, 0x00, 0x54, 0xFF, 0xEF, 0x00, 0x00, 0xFA, 0x80, 0x00, 0x0B, 0x12, 0x82, 0x00, 0x01,
        0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x28, 0x00, 0x00, 0xFF, 0xFF, 0x45, 0x81, 0xFF, 0xFF, 0xFA, 0x72, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x03, 0xE8, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x7F, 0xFF, 0xFF, 0xFE, 0x80, 0x01,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x3E, 0x03, 0x30, 0x40, 0x00, 0x00, 0x00, 0x02, 0xCA, 0xE3, 0x09, 0x3E, 0x80, 0x00, 0x00,
        0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x00,
        0x41, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x0B, 0x2A, 0x00, 0x00, 0x16, 0x55, 0x00, 0x00, 0x21, 0x82,
        0xFD, 0x87, 0x26, 0x50, 0xFD, 0x80, 0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x05, 0x80, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x6F, 0x00, 0x02, 0x65, 0x32, 0x00, 0x00, 0x5E, 0xC0,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0xFB, 0x8C, 0x6F, 0x5D, 0xFD, 0x5D, 0x08, 0xD9, 0x00, 0x7C, 0x73, 0x3B, 0x00, 0x6C, 0x12, 0xCC,
        0x32, 0x00, 0x13, 0x9D, 0x32, 0x00, 0xD0, 0xD6, 0x32, 0x00, 0x08, 0x00, 0x40, 0x00, 0x01, 0xF4,
        0xFF, 0xE6, 0x80, 0x79, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0xD0, 0xD6, 0x00, 0x00, 0x27, 0x10,

        # bank 1, 256 bytes
        0xFB, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00,
        0x00, 0x00, 0xFA, 0x36, 0xFF, 0xBC, 0x30, 0x8E, 0x00, 0x05, 0xFB, 0xF0, 0xFF, 0xD9, 0x5B, 0xC8,
        0xFF, 0xD0, 0x9A, 0xBE, 0x00, 0x00, 0x10, 0xA9, 0xFF, 0xF4, 0x1E, 0xB2, 0x00, 0xCE, 0xBB, 0xF7,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x04, 0x00, 0x02, 0x00, 0x02, 0x02, 0x00, 0x00, 0x0C,
        0xFF, 0xC2, 0x80, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0xCF, 0x80, 0x00, 0x40, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x14,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x03, 0x3F, 0x68, 0xB6, 0x79, 0x35, 0x28, 0xBC, 0xC6, 0x7E, 0xD1, 0x6C,
        0x80, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0xB2, 0x6A, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x3F, 0xF0, 0x00, 0x00, 0x00, 0x30,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x25, 0x4D, 0x00, 0x2F, 0x70, 0x6D, 0x00, 0x00, 0x05, 0xAE, 0x00, 0x0C, 0x02, 0xD0,

        # bank 2, 256 bytes
        0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x00, 0x54, 0xFF, 0xEF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x01, 0x00, 0x00, 0x44, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x01, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x65, 0x00, 0x00, 0x00, 0x54, 0x00, 0x00, 0xFF, 0xEF, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x40, 0x00, 0x00, 0x00,
        0x00, 0x1B, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,

        # bank 3, 256 bytes
        0xD8, 0xDC, 0xBA, 0xA2, 0xF1, 0xDE, 0xB2, 0xB8, 0xB4, 0xA8, 0x81, 0x91, 0xF7, 0x4A, 0x90, 0x7F,
        0x91, 0x6A, 0xF3, 0xF9, 0xDB, 0xA8, 0xF9, 0xB0, 0xBA, 0xA0, 0x80, 0xF2, 0xCE, 0x81, 0xF3, 0xC2,
        0xF1, 0xC1, 0xF2, 0xC3, 0xF3, 0xCC, 0xA2, 0xB2, 0x80, 0xF1, 0xC6, 0xD8, 0x80, 0xBA, 0xA7, 0xDF,
        0xDF, 0xDF, 0xF2, 0xA7, 0xC3, 0xCB, 0xC5, 0xB6, 0xF0, 0x87, 0xA2, 0x94, 0x24, 0x48, 0x70, 0x3C,
        0x95, 0x40, 0x68, 0x34, 0x58, 0x9B, 0x78, 0xA2, 0xF1, 0x83, 0x92, 0x2D, 0x55, 0x7D, 0xD8, 0xB1,
        0xB4, 0xB8, 0xA1, 0xD0, 0x91, 0x80, 0xF2, 0x70, 0xF3, 0x70, 0xF2, 0x7C, 0x80, 0xA8, 0xF1, 0x01,
        0xB0, 0x98, 0x87, 0xD9, 0x43, 0xD8, 0x86, 0xC9, 0x88, 0xBA, 0xA1, 0xF2, 0x0E, 0xB8, 0x97, 0x80,
        0xF1, 0xA9, 0xDF, 0xDF, 0xDF, 0xAA, 0xDF, 0xDF, 0xDF, 0xF2, 0xAA, 0xC5, 0xCD, 0xC7, 0xA9, 0x0C,
        0xC9, 0x2C, 0x97, 0x97, 0x97, 0x97, 0xF1, 0xA9, 0x89, 0x26, 0x46, 0x66, 0xB0, 0xB4, 0xBA, 0x80,
        0xAC, 0xDE, 0xF2, 0xCA, 0xF1, 0xB2, 0x8C, 0x02, 0xA9, 0xB6, 0x98, 0x00, 0x89, 0x0E, 0x16, 0x1E,
        0xB8, 0xA9, 0xB4, 0x99, 0x2C, 0x54, 0x7C, 0xB0, 0x8A, 0xA8, 0x96, 0x36, 0x56, 0x76, 0xF1, 0xB9,
        0xAF, 0xB4, 0xB0, 0x83, 0xC0, 0xB8, 0xA8, 0x97, 0x11, 0xB1, 0x8F, 0x98, 0xB9, 0xAF, 0xF0, 0x24,
        0x08, 0x44, 0x10, 0x64, 0x18, 0xF1, 0xA3, 0x29, 0x55, 0x7D, 0xAF, 0x83, 0xB5, 0x93, 0xAF, 0xF0,
        0x00, 0x28, 0x50, 0xF1, 0xA3, 0x86, 0x9F, 0x61, 0xA6, 0xDA, 0xDE, 0xDF, 0xD9, 0xFA, 0xA3, 0x86,
        0x96, 0xDB, 0x31, 0xA6, 0xD9, 0xF8, 0xDF, 0xBA, 0xA6, 0x8F, 0xC2, 0xC5, 0xC7, 0xB2, 0x8C, 0xC1,
        0xB8, 0xA2, 0xDF, 0xDF, 0xDF, 0xA3, 0xDF, 0xDF, 0xDF, 0xD8, 0xD8, 0xF1, 0xB8, 0xA8, 0xB2, 0x86,

        # bank 4, 256 bytes
        0xB4, 0x98, 0x0D, 0x35, 0x5D, 0xB8, 0xAA, 0x98, 0xB0, 0x87, 0x2D, 0x35, 0x3D, 0xB2, 0xB6, 0xBA,
        0xAF, 0x8C, 0x96, 0x19, 0x8F, 0x9F, 0xA7, 0x0E, 0x16, 0x1E, 0xB4, 0x9A, 0xB8, 0xAA, 0x87, 0x2C,
        0x54, 0x7C, 0xB9, 0xA3, 0xDE, 0xDF, 0xDF, 0xA3, 0xB1, 0x80, 0xF2, 0xC4, 0xCD, 0xC9, 0xF1, 0xB8,
        0xA9, 0xB4, 0x99, 0x83, 0x0D, 0x35, 0x5D, 0x89, 0xB9, 0xA3, 0x2D, 0x55, 0x7D, 0xB5, 0x93, 0xA3,
        0x0E, 0x16, 0x1E, 0xA9, 0x2C, 0x54, 0x7C, 0xB8, 0xB4, 0xB0, 0xF1, 0x97, 0x83, 0xA8, 0x11, 0x84,
        0xA5, 0x09, 0x98, 0xA3, 0x83, 0xF0, 0xDA, 0x24, 0x08, 0x44, 0x10, 0x64, 0x18, 0xD8, 0xF1, 0xA5,
        0x29, 0x55, 0x7D, 0xA5, 0x85, 0x95, 0x02, 0x1A, 0x2E, 0x3A, 0x56, 0x5A, 0x40, 0x48, 0xF9, 0xF3,
        0xA3, 0xD9, 0xF8, 0xF0, 0x98, 0x83, 0x24, 0x08, 0x44, 0x10, 0x64, 0x18, 0x97, 0x82, 0xA8, 0xF1,
        0x11, 0xF0, 0x98, 0xA2, 0x24, 0x08, 0x44, 0x10, 0x64, 0x18, 0xDA, 0xF3, 0xDE, 0xD8, 0x83, 0xA5,
        0x94, 0x01, 0xD9, 0xA3, 0x02, 0xF1, 0xA2, 0xC3, 0xC5, 0xC7, 0xD8, 0xF1, 0x84, 0x92, 0xA2, 0x4D,
        0xDA, 0x2A, 0xD8, 0x48, 0x69, 0xD9, 0x2A, 0xD8, 0x68, 0x55, 0xDA, 0x32, 0xD8, 0x50, 0x71, 0xD9,
        0x32, 0xD8, 0x70, 0x5D, 0xDA, 0x3A, 0xD8, 0x58, 0x79, 0xD9, 0x3A, 0xD8, 0x78, 0x93, 0xA3, 0x4D,
        0xDA, 0x2A, 0xD8, 0x48, 0x69, 0xD9, 0x2A, 0xD8, 0x68, 0x55, 0xDA, 0x32, 0xD8, 0x50, 0x71, 0xD9,
        0x32, 0xD8, 0x70, 0x5D, 0xDA, 0x3A, 0xD8, 0x58, 0x79, 0xD9, 0x3A, 0xD8, 0x78, 0xA8, 0x8A, 0x9A,
        0xF0, 0x28, 0x50, 0x78, 0x9E, 0xF3, 0x88, 0x18, 0xF1, 0x9F, 0x1D, 0x98, 0xA8, 0xD9, 0x08, 0xD8,
        0xC8, 0x9F, 0x12, 0x9E, 0xF3, 0x15, 0xA8, 0xDA, 0x12, 0x10, 0xD8, 0xF1, 0xAF, 0xC8, 0x97, 0x87,

        # bank 5, 256 bytes
        0x34, 0xB5, 0xB9, 0x94, 0xA4, 0x21, 0xF3, 0xD9, 0x22, 0xD8, 0xF2, 0x2D, 0xF3, 0xD9, 0x2A, 0xD8,
        0xF2, 0x35, 0xF3, 0xD9, 0x32, 0xD8, 0x81, 0xA4, 0x60, 0x60, 0x61, 0xD9, 0x61, 0xD8, 0x6C, 0x68,
        0x69, 0xD9, 0x69, 0xD8, 0x74, 0x70, 0x71, 0xD9, 0x71, 0xD8, 0xB1, 0xA3, 0x84, 0x19, 0x3D, 0x5D,
        0xA3, 0x83, 0x1A, 0x3E, 0x5E, 0x93, 0x10, 0x30, 0x81, 0x10, 0x11, 0xB8, 0xB0, 0xAF, 0x8F, 0x94,
        0xF2, 0xDA, 0x3E, 0xD8, 0xB4, 0x9A, 0xA8, 0x87, 0x29, 0xDA, 0xF8, 0xD8, 0x87, 0x9A, 0x35, 0xDA,
        0xF8, 0xD8, 0x87, 0x9A, 0x3D, 0xDA, 0xF8, 0xD8, 0xB1, 0xB9, 0xA4, 0x98, 0x85, 0x02, 0x2E, 0x56,
        0xA5, 0x81, 0x00, 0x0C, 0x14, 0xA3, 0x97, 0xB0, 0x8A, 0xF1, 0x2D, 0xD9, 0x28, 0xD8, 0x4D, 0xD9,
        0x48, 0xD8, 0x6D, 0xD9, 0x68, 0xD8, 0xB1, 0x84, 0x0D, 0xDA, 0x0E, 0xD8, 0xA3, 0x29, 0x83, 0xDA,
        0x2C, 0x0E, 0xD8, 0xA3, 0x84, 0x49, 0x83, 0xDA, 0x2C, 0x4C, 0x0E, 0xD8, 0xB8, 0xB0, 0xA8, 0x8A,
        0x9A, 0xF5, 0x20, 0xAA, 0xDA, 0xDF, 0xD8, 0xA8, 0x40, 0xAA, 0xD0, 0xDA, 0xDE, 0xD8, 0xA8, 0x60,
        0xAA, 0xDA, 0xD0, 0xDF, 0xD8, 0xF1, 0x97, 0x86, 0xA8, 0x31, 0x9B, 0x06, 0x99, 0x07, 0xAB, 0x97,
        0x28, 0x88, 0x9B, 0xF0, 0x0C, 0x20, 0x14, 0x40, 0xB8, 0xB0, 0xB4, 0xA8, 0x8C, 0x9C, 0xF0, 0x04,
        0x28, 0x51, 0x79, 0x1D, 0x30, 0x14, 0x38, 0xB2, 0x82, 0xAB, 0xD0, 0x98, 0x2C, 0x50, 0x50, 0x78,
        0x78, 0x9B, 0xF1, 0x1A, 0xB0, 0xF0, 0x8A, 0x9C, 0xA8, 0x29, 0x51, 0x79, 0x8B, 0x29, 0x51, 0x79,
        0x8A, 0x24, 0x70, 0x59, 0x8B, 0x20, 0x58, 0x71, 0x8A, 0x44, 0x69, 0x38, 0x8B, 0x39, 0x40, 0x68,
        0x8A, 0x64, 0x48, 0x31, 0x8B, 0x30, 0x49, 0x60, 0xA5, 0x88, 0x20, 0x09, 0x71, 0x58, 0x44, 0x68,

        # bank 6, 256 bytes
        0x11, 0x39, 0x64, 0x49, 0x30, 0x19, 0xF1, 0xAC, 0x00, 0x2C, 0x54, 0x7C, 0xF0, 0x8C, 0xA8, 0x04,
        0x28, 0x50, 0x78, 0xF1, 0x88, 0x97, 0x26, 0xA8, 0x59, 0x98, 0xAC, 0x8C, 0x02, 0x26, 0x46, 0x66,
        0xF0, 0x89, 0x9C, 0xA8, 0x29, 0x51, 0x79, 0x24, 0x70, 0x59, 0x44, 0x69, 0x38, 0x64, 0x48, 0x31,
        0xA9, 0x88, 0x09, 0x20, 0x59, 0x70, 0xAB, 0x11, 0x38, 0x40, 0x69, 0xA8, 0x19, 0x31, 0x48, 0x60,
        0x8C, 0xA8, 0x3C, 0x41, 0x5C, 0x20, 0x7C, 0x00, 0xF1, 0x87, 0x98, 0x19, 0x86, 0xA8, 0x6E, 0x76,
        0x7E, 0xA9, 0x99, 0x88, 0x2D, 0x55, 0x7D, 0x9E, 0xB9, 0xA3, 0x8A, 0x22, 0x8A, 0x6E, 0x8A, 0x56,
        0x8A, 0x5E, 0x9F, 0xB1, 0x83, 0x06, 0x26, 0x46, 0x66, 0x0E, 0x2E, 0x4E, 0x6E, 0x9D, 0xB8, 0xAD,
        0x00, 0x2C, 0x54, 0x7C, 0xF2, 0xB1, 0x8C, 0xB4, 0x99, 0xB9, 0xA3, 0x2D, 0x55, 0x7D, 0x81, 0x91,
        0xAC, 0x38, 0xAD, 0x3A, 0xB5, 0x83, 0x91, 0xAC, 0x2D, 0xD9, 0x28, 0xD8, 0x4D, 0xD9, 0x48, 0xD8,
        0x6D, 0xD9, 0x68, 0xD8, 0x8C, 0x9D, 0xAE, 0x29, 0xD9, 0x04, 0xAE, 0xD8, 0x51, 0xD9, 0x04, 0xAE,
        0xD8, 0x79, 0xD9, 0x04, 0xD8, 0x81, 0xF3, 0x9D, 0xAD, 0x00, 0x8D, 0xAE, 0x19, 0x81, 0xAD, 0xD9,
        0x01, 0xD8, 0xF2, 0xAE, 0xDA, 0x26, 0xD8, 0x8E, 0x91, 0x29, 0x83, 0xA7, 0xD9, 0xAD, 0xAD, 0xAD,
        0xAD, 0xF3, 0x2A, 0xD8, 0xD8, 0xF1, 0xB0, 0xAC, 0x89, 0x91, 0x3E, 0x5E, 0x76, 0xF3, 0xAC, 0x2E,
        0x2E, 0xF1, 0xB1, 0x8C, 0x5A, 0x9C, 0xAC, 0x2C, 0x28, 0x28, 0x28, 0x9C, 0xAC, 0x30, 0x18, 0xA8,
        0x98, 0x81, 0x28, 0x34, 0x3C, 0x97, 0x24, 0xA7, 0x28, 0x34, 0x3C, 0x9C, 0x24, 0xF2, 0xB0, 0x89,
        0xAC, 0x91, 0x2C, 0x4C, 0x6C, 0x8A, 0x9B, 0x2D, 0xD9, 0xD8, 0xD8, 0x51, 0xD9, 0xD8, 0xD8, 0x79,

        # bank 7, 138 bytes (remainder)
        0xD9, 0xD8, 0xD8, 0xF1, 0x9E, 0x88, 0xA3, 0x31, 0xDA, 0xD8, 0xD8, 0x91, 0x2D, 0xD9, 0x28, 0xD8,
        0x4D, 0xD9, 0x48, 0xD8, 0x6D, 0xD9, 0x68, 0xD8, 0xB1, 0x83, 0x93, 0x35, 0x3D, 0x80, 0x25, 0xDA,
        0xD8, 0xD8, 0x85, 0x69, 0xDA, 0xD8, 0xD8, 0xB4, 0x93, 0x81, 0xA3, 0x28, 0x34, 0x3C, 0xF3, 0xAB,
        0x8B, 0xF8, 0xA3, 0x91, 0xB6, 0x09, 0xB4, 0xD9, 0xAB, 0xDE, 0xFA, 0xB0, 0x87, 0x9C, 0xB9, 0xA3,
        0xDD, 0xF1, 0xA3, 0xA3, 0xA3, 0xA3, 0x95, 0xF1, 0xA3, 0xA3, 0xA3, 0x9D, 0xF1, 0xA3, 0xA3, 0xA3,
        0xA3, 0xF2, 0xA3, 0xB4, 0x90, 0x80, 0xF2, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3,
        0xA3, 0xB2, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xA3, 0xB0, 0x87, 0xB5, 0x99, 0xF1, 0xA3, 0xA3, 0xA3,
        0x98, 0xF1, 0xA3, 0xA3, 0xA3, 0xA3, 0x97, 0xA3, 0xA3, 0xA3, 0xA3, 0xF3, 0x9B, 0xA3, 0xA3, 0xDC,
        0xB9, 0xA7, 0xF1, 0x26, 0x26, 0x26, 0xD8, 0xD8, 0xFF]
    
    dmpConfig = [
        # BANK    OFFSET  LENGTH  [DATA]
        0x03,   0x7B,   0x03,   0x4C, 0xCD, 0x6C,         # FCFG_1 inv_set_gyro_calibration
        0x03,   0xAB,   0x03,   0x36, 0x56, 0x76,         # FCFG_3 inv_set_gyro_calibration
        0x00,   0x68,   0x04,   0x02, 0xCB, 0x47, 0xA2,   # D_0_104 inv_set_gyro_calibration
        0x02,   0x18,   0x04,   0x00, 0x05, 0x8B, 0xC1,   # D_0_24 inv_set_gyro_calibration
        0x01,   0x0C,   0x04,   0x00, 0x00, 0x00, 0x00,   # D_1_152 inv_set_accel_calibration
        0x03,   0x7F,   0x06,   0x0C, 0xC9, 0x2C, 0x97, 0x97, 0x97, # FCFG_2 inv_set_accel_calibration
        0x03,   0x89,   0x03,   0x26, 0x46, 0x66,         # FCFG_7 inv_set_accel_calibration
        0x00,   0x6C,   0x02,   0x20, 0x00,               # D_0_108 inv_set_accel_calibration
        0x02,   0x40,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_00 inv_set_compass_calibration
        0x02,   0x44,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_01
        0x02,   0x48,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_02
        0x02,   0x4C,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_10
        0x02,   0x50,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_11
        0x02,   0x54,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_12
        0x02,   0x58,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_20
        0x02,   0x5C,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_21
        0x02,   0xBC,   0x04,   0x00, 0x00, 0x00, 0x00,   # CPASS_MTX_22
        0x01,   0xEC,   0x04,   0x00, 0x00, 0x40, 0x00,   # D_1_236 inv_apply_endian_accel
        0x03,   0x7F,   0x06,   0x0C, 0xC9, 0x2C, 0x97, 0x97, 0x97, # FCFG_2 inv_set_mpu_sensors
        0x04,   0x02,   0x03,   0x0D, 0x35, 0x5D,         # CFG_MOTION_BIAS inv_turn_on_bias_from_no_motion
        0x04,   0x09,   0x04,   0x87, 0x2D, 0x35, 0x3D,   # FCFG_5 inv_set_bias_update
        0x00,   0xA3,   0x01,   0x00,                     # D_0_163 inv_set_dead_zone
        # SPECIAL 0x01 = enable interrupts
        0x00,   0x00,   0x00,   0x01, # SET INT_ENABLE at i=22, SPECIAL INSTRUCTION
        0x07,   0x86,   0x01,   0xFE,                     # CFG_6 inv_set_fifo_interupt
        0x07,   0x41,   0x05,   0xF1, 0x20, 0x28, 0x30, 0x38, # CFG_8 inv_send_quaternion
        0x07,   0x7E,   0x01,   0x30,                     # CFG_16 inv_set_footer
        0x07,   0x46,   0x01,   0x9A,                     # CFG_GYRO_SOURCE inv_send_gyro
        0x07,   0x47,   0x04,   0xF1, 0x28, 0x30, 0x38,   # CFG_9 inv_send_gyro -> inv_construct3_fifo
        0x07,   0x6C,   0x04,   0xF1, 0x28, 0x30, 0x38,   # CFG_12 inv_send_accel -> inv_construct3_fifo
        0x02,   0x16,   0x02,   0x00, 0x05                # D_0_22 inv_set_fifo_rate

        
        # This very last 0x01 WAS a 0x09, which drops the FIFO rate down to 20 Hz. 0x07 is 25 Hz,
        # 0x01 is 100Hz. Going faster than 100Hz (0x00=200Hz) tends to result in very noisy data.
        # DMP output frequency is calculated easily using this equation: (200Hz / (1 + value))

        # It is important to make sure the host processor can keep up with reading and processing
        # the FIFO output at the desired rate. Handling FIFO overflow cleanly is also a good idea.    
        ]
    
    dmpUpdates = [
        0x01,   0xB2,   0x02,   0xFF, 0xFF,
        0x01,   0x90,   0x04,   0x09, 0x23, 0xA1, 0x35,
        0x01,   0x6A,   0x02,   0x06, 0x00,
        0x01,   0x60,   0x08,   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00,   0x60,   0x04,   0x40, 0x00, 0x00, 0x00,
        0x01,   0x62,   0x02,   0x00, 0x00,
        0x00,   0x60,   0x04,   0x00, 0x40, 0x00, 0x00]
    
    # Setting up internal 42-byte (default) DMP packet buffer
    dmpPacketSize = 42
    
    # construct a new object with the I2C address of the MPU6050
    def __init__(self, address = MPU6050_DEFAULT_ADDRESS):
        self.i2c = PyComms(address)
        self.address = address
        
    def initialize(self):
        self.setClockSource(self.MPU6050_CLOCK_PLL_XGYRO)
        self.setFullScaleGyroRange(self.MPU6050_GYRO_FS_250)
        self.setFullScaleAccelRange(self.MPU6050_ACCEL_FS_2)   
        self.setSleepEnabled(False)
        
    def testConnection(self):
        return self.getDeviceID() == 0x34
    
    def getAuxVDDIOLevel(self):
        return self.i2c.readBit(self.MPU6050_RA_YG_OFFS_TC, self.MPU6050_TC_PWR_MODE_BIT)
        
    def setAuxVDDIOLevel(self, level):
        self.i2c.writeBit(self.MPU6050_RA_YG_OFFS_TC, self.MPU6050_TC_PWR_MODE_BIT, level)
    
    def getRate(self):
        return self.i2c.readU8(self.MPU6050_RA_SMPLRT_DIV)
        
    def setRate(self, value):
        self.i2c.write8(self.MPU6050_RA_SMPLRT_DIV, value)
    
    def getExternalFrameSync(self):
        return self.i2c.readBits(self.MPU6050_RA_CONFIG, self.MPU6050_CFG_EXT_SYNC_SET_BIT, self.MPU6050_CFG_EXT_SYNC_SET_LENGTH)

    def setExternalFrameSync(self, sync):
        self.i2c.writeBits(self.MPU6050_RA_CONFIG, self.MPU6050_CFG_EXT_SYNC_SET_BIT, self.MPU6050_CFG_EXT_SYNC_SET_LENGTH, sync)
    
    def getDLPFMode(self):
        return self.i2c.readBits(self.MPU6050_RA_CONFIG, self.MPU6050_CFG_DLPF_CFG_BIT, self.MPU6050_CFG_DLPF_CFG_LENGTH)
        
    def setDLPFMode(self, mode):
        self.i2c.writeBits(self.MPU6050_RA_CONFIG, self.MPU6050_CFG_DLPF_CFG_BIT, self.MPU6050_CFG_DLPF_CFG_LENGTH, mode)
     
    def getFullScaleGyroRange(self):
        return self.i2c.readBits(self.MPU6050_RA_GYRO_CONFIG, self.MPU6050_GCONFIG_FS_SEL_BIT, self.MPU6050_GCONFIG_FS_SEL_LENGTH)

    def setFullScaleGyroRange(self, range):
        self.i2c.writeBits(self.MPU6050_RA_GYRO_CONFIG, self.MPU6050_GCONFIG_FS_SEL_BIT, self.MPU6050_GCONFIG_FS_SEL_LENGTH, range)        
    
    def getAccelXSelfTest(self):
        return self.i2c.readBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_XA_ST_BIT)

    def setAccelXSelfTest(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_XA_ST_BIT, enabled)

    def getAccelYSelfTest(self):
        return self.readBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_YA_ST_BIT)
        
    def setAccelYSelfTest(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_YA_ST_BIT, enabled)

    def getAccelZSelfTest(self):
        return self.i2c.readBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_ZA_ST_BIT)
    
    def setAccelZSelfTest(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_ZA_ST_BIT, enabled)

    def getFullScaleAccelRange(self):
        return self.i2c.readBits(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_AFS_SEL_BIT, self.MPU6050_ACONFIG_AFS_SEL_LENGTH)
        
    def setFullScaleAccelRange(self, value):
        self.i2c.writeBits(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_AFS_SEL_BIT, self.MPU6050_ACONFIG_AFS_SEL_LENGTH, value)
            
    def getDHPFMode(self):
        return self.i2c.readBits(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_ACCEL_HPF_BIT, self.MPU6050_ACONFIG_ACCEL_HPF_LENGTH)

    def setDHPFMode(self, bandwith):
        self.i2c.writeBits(self.MPU6050_RA_ACCEL_CONFIG, self.MPU6050_ACONFIG_ACCEL_HPF_BIT, self.MPU6050_ACONFIG_ACCEL_HPF_LENGTH, bandwidth)

    def getFreefallDetectionThreshold(self):
        return self.i2c.readU8(self.MPU6050_RA_FF_THR)
        
    def setFreefallDetectionThreshold(self, treshold):
        self.i2c.write8(self.MPU6050_RA_FF_THR, treshold)

    def getFreefallDetectionDuration(self):
        return self.i2c.readU8(self.MPU6050_RA_FF_DUR)

    def setFreefallDetectionDuration(self, duration):
        self.i2c.write8(self.MPU6050_RA_FF_DUR)
    
    def getMotionDetectionThreshold(self):
        return self.i2c.readU8(self.MPU6050_RA_MOT_THR)
        
    def setMotionDetectionThreshold(self, treshold):
        self.i2c.write8(self.MPU6050_RA_MOT_THR, treshold)    

    def getMotionDetectionDuration(self):
        return self.i2c.readU8(self.MPU6050_RA_MOT_DUR)

    def setMotionDetectionDuration(self, duration):
        self.i2c.write8(self.MPU6050_RA_MOT_DUR, duration)

    def getZeroMotionDetectionThreshold(self):
        return self.i2c.readU8(self.MPU6050_RA_ZRMOT_THR)

    def setZeroMotionDetectionThreshold(self, treshold):
        self.i2c.write8(self.MPU6050_RA_ZRMOT_THR, treshold)

    def getZeroMotionDetectionDuration(self):
        return self.i2c.readU8(self.MPU6050_RA_ZRMOT_DUR)

    def setZeroMotionDetectionDuration(self, duration):
        self.i2c.write8(self.MPU6050_RA_ZRMOT_DUR, duration)
        
    def getTempFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_TEMP_FIFO_EN_BIT)
        
    def setTempFIFOEnabled(self, enabled):
        self.i2c.write8(self.MPU6050_RA_FIFO_EN, self.MPU6050_TEMP_FIFO_EN_BIT, enabled)
        
    def getXGyroFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_XG_FIFO_EN_BIT)
        
    def setXGyroFIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_XG_FIFO_EN_BIT, enabled)
        
    def getYGyroFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_YG_FIFO_EN_BIT)
        
    def setYGyroFIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_YG_FIFO_EN_BIT, enabled)
        
    def getZGyroFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_ZG_FIFO_EN_BIT)
        
    def setZGyroFIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_ZG_FIFO_EN_BIT, enabled)
        
    def getAccelFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_ACCEL_FIFO_EN_BIT)
        
    def setAccelFIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_ACCEL_FIFO_EN_BIT, enabled)
        
    def getSlave2FIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV2_FIFO_EN_BIT)
        
    def setSlave2FIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV2_FIFO_EN_BIT, enabled)
        
    def getSlave1FIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV1_FIFO_EN_BIT)
        
    def setSlave1FIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV1_FIFO_EN_BIT, enabled)
        
    def getSlave0FIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV0_FIFO_EN_BIT)
        
    def setSlave0FIFOEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_FIFO_EN, self.MPU6050_SLV0_FIFO_EN_BIT, enabled)
        
    def getMultiMasterEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_MULT_MST_EN_BIT)
        
    def setMultiMasterEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_MULT_MST_EN_BIT, enabled)
        
    def getWaitForExternalSensorEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_WAIT_FOR_ES_BIT)
        
    def setWaitForExternalSensorEnabled(self, value):
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_WAIT_FOR_ES_BIT, enabled)
        
    def getSlave3FIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_SLV_3_FIFO_EN_BIT)
        
    def setSlave3FIFOEnabled(self, enabled):    
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_SLV_3_FIFO_EN_BIT, enabled)
        
    def getSlaveReadWriteTransitionEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_I2C_MST_P_NSR_BIT)
        
    def setSlaveReadWriteTransitionEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_I2C_MST_P_NSR_BIT, enabled)
        
    def getMasterClockSpeed(self):
        return self.i2c.readBits(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_I2C_MST_CLK_BIT, self.MPU6050_I2C_MST_CLK_LENGTH)
        
    def setMasterClockSpeed(self, speed):
        self.i2c.writeBits(self.MPU6050_RA_I2C_MST_CTRL, self.MPU6050_I2C_MST_CLK_BIT, self.MPU6050_I2C_MST_CLK_LENGTH, speed)
        
    def getSlaveAddress(self, num):
        if num > 3:
            return 0
            
        return self.i2c.readU8(self.MPU6050_RA_I2C_SLV0_ADDR + num * 3)    
        
    def setSlaveAddress(self, num, address):
        if num > 3:
            return
        self.i2c.write8(self.MPU6050_RA_I2C_SLV0_ADDR + num * 3, address)        
        
    def getSlaveRegister(self, num):
        if num > 3:
            return 0
        
        return self.i2c.readU8(self.MPU6050_RA_I2C_SLV0_REG + num * 3)
        
    def setSlaveRegister(self, num, reg):
        if num > 3:
            return
        self.i2c.write8(self.MPU6050_RA_I2C_SLV0_REG + num * 3, reg)      
        
    def getSlaveEnabled(self, num):
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_EN_BIT)
        
    def setSlaveEnabled(self, num, enabled):
        if num > 3:
            return
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_EN_BIT, enabled)    
        
    def getSlaveWordByteSwap(self, num):
        if num > 3:
            return 0
            
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_BYTE_SW_BIT)    
        
    def setSlaveWordByteSwap(self, num, enabled):
        if num > 3:
            return
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_BYTE_SW_BIT, enabled)    
            
        
    def getSlaveWriteMode(self, num):
        if num > 3:
            return 0
            
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_REG_DIS_BIT)    
        
    def setSlaveWriteMode(self, num, mode):
        if num > 3:
            return
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_REG_DIS_BIT, mode)    
        
    def getSlaveWordGroupOffset(self, num):
        if num > 3:
            return 0
            
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_GRP_BIT)    
        
    def setSlaveWordGroupOffset(self, num, enabled):
        if num > 3:
            return
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_GRP_BIT, enabled)    
        
    def getSlaveDataLength(self, num):
        if num > 3:
            return 0
        
        return self.i2c.readBits(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_LEN_BIT, self.MPU6050_I2C_SLV_LEN_LENGTH)
        
    def setSlaveDataLength(self, num, length):
        if num > 3:
            return
        self.i2c.writeBits(self.MPU6050_RA_I2C_SLV0_CTRL + num * 3, self.MPU6050_I2C_SLV_LEN_BIT, self.MPU6050_I2C_SLV_LEN_LENGTH, length)
        
    def getSlave4Address(self):
        return self.i2c.readU8(self.MPU6050_RA_I2C_SLV4_ADDR)
        
    def setSlave4Address(self, address):
        self.i2c.write8(self.MPU6050_RA_I2C_SLV4_ADDR, address)
        
    def getSlave4Register(self):
        return self.i2c.readU8(self.MPU6050_RA_I2C_SLV4_REG)
        
    def setSlave4Register(self, reg):
        self.i2c.write8(self.MPU6050_RA_I2C_SLV4_REG, reg)
        
    def setSlave4OutputByte(self, data):
        self.i2c.write8(self.MPU6050_RA_I2C_SLV4_DO, data)
        
    def getSlave4Enabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_EN_BIT)
        
    def setSlave4Enabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_EN_BIT, enabled)
        
    def getSlave4InterruptEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_INT_EN_BIT)
        
    def setSlave4InterruptEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_INT_EN_BIT, enabled)
        
    def getSlave4WriteMode(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_REG_DIS_BIT)
        
    def setSlave4WriteMode(self, mode):
        self.i2c.writeBit(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_REG_DIS_BIT, mode)
        
    def getSlave4MasterDelay(self):
        return self.i2c.readBits(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_MST_DLY_BIT, self.MPU6050_I2C_SLV4_MST_DLY_LENGTH)
        
    def setSlave4MasterDelay(self, delay):
        self.i2c.writeBits(self.MPU6050_RA_I2C_SLV4_CTRL, self.MPU6050_I2C_SLV4_MST_DLY_BIT, self.MPU6050_I2C_SLV4_MST_DLY_LENGTH, delay)
        
    def getSlate4InputByte(self):
        return self.i2c.readU8(self.MPU6050_RA_I2C_SLV4_DI)
        
    def getPassthroughStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_PASS_THROUGH_BIT)
        
    def getSlave4IsDone(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV4_DONE_BIT)
        
    def getLostArbitration(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_LOST_ARB_BIT)
        
    def getSlave4Nack(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV4_NACK_BIT)
        
    def getSlave3Nack(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV3_NACK_BIT)
        
    def getSlave2Nack(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV2_NACK_BIT)
        
    def getSlave1Nack(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV1_NACK_BIT)
        
    def getSlave0Nack(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_STATUS, self.MPU6050_MST_I2C_SLV0_NACK_BIT)
        
    def getInterruptMode(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_LEVEL_BIT)
        
    def setInterruptMode(self, mode):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_LEVEL_BIT, mode)
        
    def getInterruptDrive(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_OPEN_BIT)
        
    def setInterruptDrive(self, drive):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_OPEN_BIT, drive)
        
    def getInterruptLatch(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_LATCH_INT_EN_BIT)

    def setInterruptLatch(self, latch):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_LATCH_INT_EN_BIT, latch)

    def getInterruptLatchClear(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_RD_CLEAR_BIT)
    
    def setInterruptLatchClear(self, clear):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_INT_RD_CLEAR_BIT, clear)

    def getFSyncInterruptLevel(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_FSYNC_INT_LEVEL_BIT)

    def setFSyncInterruptLevel(self, level):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_FSYNC_INT_LEVEL_BIT, level)

    def getFSyncInterruptEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_FSYNC_INT_EN_BIT)

    def setFSyncInterruptEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_FSYNC_INT_EN_BIT, enabled)

    def getI2CBypassEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_I2C_BYPASS_EN_BIT)

    def setI2CBypassEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_I2C_BYPASS_EN_BIT, enabled)

    def getClockOutputEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_CLKOUT_EN_BIT)

    def setClockOutputEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_PIN_CFG, self.MPU6050_INTCFG_CLKOUT_EN_BIT, enabled)

    def getIntEnabled(self):
        return self.i2c.readU8(self.MPU6050_RA_INT_ENABLE)

    def setIntEnabled(self, status):
        self.i2c.write8(self.MPU6050_RA_INT_ENABLE, status)        
        
    def getIntFreefallEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_FF_BIT)
        
    def setIntFreefallEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_FF_BIT, enabled)
        
    def getIntMotionEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_MOT_BIT)
        
    def setIntMotionEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_MOT_BIT, enabled)
        
    def getIntZeroMotionEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_ZMOT_BIT)
        
    def setIntZeroMotionEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_ZMOT_BIT, enabled)
        
    def getIntFIFOBufferOverflowEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_FIFO_OFLOW_BIT)
        
    def setIntFIFOBufferOverflowEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_FIFO_OFLOW_BIT, enabled)
        
    def getIntI2CMasterEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_I2C_MST_INT_BIT)
        
    def setIntI2CMasterEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_I2C_MST_INT_BIT, enabled)
        
    def getIntDataReadyEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_DATA_RDY_BIT)
        
    def setIntDataReadyEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_DATA_RDY_BIT, enabled)

    def getIntStatus(self):
        return self.i2c.readU8(self.MPU6050_RA_INT_STATUS)

    def getIntFreefallStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_FF_BIT)

    def getIntMotionStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_MOT_BIT)

    def getIntZeroMotionStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_ZMOT_BIT)

    def getIntFIFOBufferOverflowStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_FIFO_OFLOW_BIT)

    def getIntI2CMasterStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_I2C_MST_INT_BIT)

    def getIntDataReadyStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_DATA_RDY_BIT)

    def getMotion9(self):
        # unknown
        pass

    def getMotion6(self):
        pass

    def getAcceleration(self):
        pass
        
    def getAccelerationX(self):
        pass
        
    def getAccelerationY(self):
        pass
        
    def getAccelerationZ(self):
        pass
        
    def getTemperature(self):
        pass
        
    def getRotation(self):
        pass
        
    def getRotationX(self):
        pass
        
    def getRotationY(self):
        pass
     
    def getRotationZ(self):
        pass
      
    def getExternalSensorByte(self, position):
        return self.i2c.readU8(self.MPU6050_RA_EXT_SENS_DATA_00 + position)

    def getExternalSensorWord(self, position):
        pass

    def getExternalSensorDWord(self, position):
        pass

    def getXNegMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_XNEG_BIT)

    def getXPosMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_XPOS_BIT)

    def getYNegMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_YNEG_BIT)

    def getYPosMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_YPOS_BIT)

    def getZNegMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_ZNEG_BIT)
    
    def getZPosMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_ZPOS_BIT)

    def getZeroMotionDetected(self):
        return self.i2c.readBit(self.MPU6050_RA_MOT_DETECT_STATUS, self.MPU6050_MOTION_MOT_ZRMOT_BIT)

    def setSlaveOutputByte(self, num, data):
        if num > 3:
            return
        self.i2c.write8(self.MPU6050_RA_I2C_SLV0_DO + num, data)    

    def getExternalShadowDelayEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_DELAY_CTRL, self.MPU6050_DELAYCTRL_DELAY_ES_SHADOW_BIT)

    def setExternalShadowDelayEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_DELAY_CTRL, self.MPU6050_DELAYCTRL_DELAY_ES_SHADOW_BIT, enabled)
      
    def getSlaveDelayEnabled(self, num):
        # // MPU6050_DELAYCTRL_I2C_SLV4_DLY_EN_BIT is 4, SLV3 is 3, etc.
        if num > 4:
            return 0
            
        return self.i2c.readBit(self.MPU6050_RA_I2C_MST_DELAY_CTRL, num)    
        
    def setSlaveDelayEnabled(self, num, enabled):
        self.i2c.writeBit(self.MPU6050_RA_I2C_MST_DELAY_CTRL, num, enabled)
        
    def resetGyroscopePath(self):
        self.i2c.writeBit(self.MPU6050_RA_SIGNAL_PATH_RESET, self.MPU6050_PATHRESET_GYRO_RESET_BIT, True)
        
    def resetAccelerometerPath(self):
        self.i2c.writeBit(self.MPU6050_RA_SIGNAL_PATH_RESET, self.MPU6050_PATHRESET_ACCEL_RESET_BIT, True)
        
    def resetTemperaturePath(self):
        self.i2c.writeBit(self.MPU6050_RA_SIGNAL_PATH_RESET, self.MPU6050_PATHRESET_TEMP_RESET_BIT, True)
        
    def getAccelerometerPowerOnDelay(self):
        return self.i2c.readBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_ACCEL_ON_DELAY_BIT, self.MPU6050_DETECT_ACCEL_ON_DELAY_LENGTH)
        
    def setAccelerometerPowerOnDelay(self, delay):
        self.i2c.writeBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_ACCEL_ON_DELAY_BIT, self.MPU6050_DETECT_ACCEL_ON_DELAY_LENGTH, delay)
        
    def getFreefallDetectionCounterDecrement(self):
        return self.i2c.readBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_FF_COUNT_BIT, self.MPU6050_DETECT_FF_COUNT_LENGTH)
        
    def setFreefallDetectionCounterDecrement(self, decrement):
        self.i2c.writeBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_FF_COUNT_BIT, self.MPU6050_DETECT_FF_COUNT_LENGTH, decrement)
        
    def getMotionDetectionCounterDecrement(self):
        return self.i2c.readBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_MOT_COUNT_BIT, self.MPU6050_DETECT_MOT_COUNT_LENGTH)
        
    def setMotionDetectionCounterDecrement(self, decrement):
        self.i2c.writeBits(self.MPU6050_RA_MOT_DETECT_CTRL, self.MPU6050_DETECT_MOT_COUNT_BIT, self.MPU6050_DETECT_MOT_COUNT_LENGTH, decrement)
        
    def getFIFOEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_FIFO_EN_BIT)
         
    def setFIFOEnabled(self, status):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_FIFO_EN_BIT, status)        
        
    def getI2CMasterModeEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_I2C_MST_EN_BIT)
        
    def setI2CMasterModeEnabled(self, status):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_I2C_MST_EN_BIT, status)        
        
    def switchSPIEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_I2C_IF_DIS_BIT, enabled)
        
    def resetFIFO(self):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_FIFO_RESET_BIT, True)           
        
    def resetI2CMaster(self):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_I2C_MST_RESET_BIT, True)        
        
    def resetSensors(self):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_SIG_COND_RESET_BIT, True)
        
    def reset(self):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_DEVICE_RESET_BIT, True)       
        
    def getSleepEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_SLEEP_BIT)
    
    def setSleepEnabled(self, status):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_SLEEP_BIT, status)        
        
    def getWakeCycleEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_CYCLE_BIT)
        
    def setWakeCycleEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_CYCLE_BIT, enabled)
        
    def getTempSensorEnabled(self):
        result = self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_TEMP_DIS_BIT)
        return result == 0 # 1 is actually disabled here
        
    def setTempSensorEnabled(self, enabled):
        # 1 is actually disabled here
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_TEMP_DIS_BIT, enabled != enabled)
        
    def getClockSource(self):
        return self.i2c.readBits(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_CLKSEL_BIT, self.MPU6050_PWR1_CLKSEL_LENGTH)
        
    def setClockSource(self, source):
        self.i2c.writeBits(self.MPU6050_RA_PWR_MGMT_1, self.MPU6050_PWR1_CLKSEL_BIT, self.MPU6050_PWR1_CLKSEL_LENGTH, source)        
        
    def getWakeFrequency(self):
        return self.i2c.readBits(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_LP_WAKE_CTRL_BIT, self.MPU6050_PWR2_LP_WAKE_CTRL_LENGTH)
        
    def setWakeFrequency(self, frequency):
        self.i2c.writeBits(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_LP_WAKE_CTRL_BIT, self.MPU6050_PWR2_LP_WAKE_CTRL_LENGTH, frequency)
        
    def getStandbyXAccelEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_XA_BIT)
        
    def setStandbyXAccelEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_XA_BIT, enabled)
        
    def getStandbyYAccelEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_YA_BIT)
        
    def setStandbyYAccelEnabled(self, enabled):  
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_YA_BIT, enabled)
        
    def getStandbyZAccelEnabled(self):    
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_ZA_BIT)
        
    def setStandbyZAccelEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_ZA_BIT, enabled)
        
    def getStandbyXGyroEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_XG_BIT)

    def setStandbyXGyroEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_XG_BIT, enabled)

    def getStandbyYGyroEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_YG_BIT)

    def setStandbyYGyroEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_YG_BIT, enabled)

    def getStandbyZGyroEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_ZG_BIT)

    def setStandbyZGyroEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_PWR_MGMT_2, self.MPU6050_PWR2_STBY_ZG_BIT, enabled)

    def getFIFOCount(self):
        return self.i2c.readU16(self.MPU6050_RA_FIFO_COUNTH)

    def getFIFOByte(self):
        return self.i2c.readU8(self.MPU6050_RA_FIFO_R_W)
    
    def getFIFOBytes(self,length):
        return self.i2c.readBytes(self.MPU6050_RA_FIFO_R_W, length)

    def setFIFOByte(self, data):
        self.i2c.write8(self.MPU6050_RA_FIFO_R_W, data)

    def getDeviceID(self):
        return self.i2c.readBits(self.MPU6050_RA_WHO_AM_I, self.MPU6050_WHO_AM_I_BIT, self.MPU6050_WHO_AM_I_LENGTH)

    def setDeviceID(self, id):
        self.i2c.writeBits(self.MPU6050_RA_WHO_AM_I, self.MPU6050_WHO_AM_I_BIT, self.MPU6050_WHO_AM_I_LENGTH, id)

    def getOTPBankValid(self):
        result = self.i2c.readBit(self.MPU6050_RA_XG_OFFS_TC, self.MPU6050_TC_OTP_BNK_VLD_BIT)
        return result
        
    def setOTPBankValid(self, status):
        self.i2c.writeBit(self.MPU6050_RA_XG_OFFS_TC, self.MPU6050_TC_OTP_BNK_VLD_BIT, status)

    def getXGyroOffset(self):
        return self.i2c.readBits(self.MPU6050_RA_XG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH)
    
    def setXGyroOffset(self, offset):
        self.i2c.writeBits(self.MPU6050_RA_XG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH, offset)

    def getYGyroOffset(self):
        return self.i2c.readBits(self.MPU6050_RA_YG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH)
    
    def setYGyroOffset(self, offset):
        self.i2c.writeBits(self.MPU6050_RA_YG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH, offset)

    def getZGyroOffset(self):
        return self.i2c.readBits(self.MPU6050_RA_ZG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH)
        
    def setZGyroOffset(self, offset):
        self.i2c.writeBits(self.MPU6050_RA_ZG_OFFS_TC, self.MPU6050_TC_OFFSET_BIT, self.MPU6050_TC_OFFSET_LENGTH, offset)        
        
    def getXFineGain(self):
        return self.i2c.readU8(self.MPU6050_RA_X_FINE_GAIN)
        
    def setXFineGain(self, gain):
        self.i2c.write8(self.MPU6050_RA_X_FINE_GAIN, gain)
        
    def getYFineGain(self):
        return self.i2c.readU8(self.MPU6050_RA_Y_FINE_GAIN)
     
    def setYFineGain(self, gain):
        self.i2c.write8(self.MPU6050_RA_Y_FINE_GAIN, gain)
     
    def getZFineGain(self):
        return self.i2c.readU8(self.MPU6050_RA_Z_FINE_GAIN)
     
    def setZFineGain(self, gain):
        self.i2c.write8(self.MPU6050_RA_Z_FINE_GAIN, gain)
    
    def getXAccelOffset(self):
        pass

    def setXAccelOffset(self, offset):
        pass

    def getYAccelOffset(self):
        pass

    def setYAccelOffset(self, offset):
        pass

    def getZAccelOffset(self):
        pass

    def setZAccelOffset(self, offset):
        pass

    def getXGyroOffsetUser(self):
        pass
        
    def setXGyroOffsetUser(self, value):
        self.i2c.write8(self.MPU6050_RA_XG_OFFS_USRH, value >> 8)
        self.i2c.write8(self.MPU6050_RA_XG_OFFS_USRL, value & 0xFF) 
        return True        
        
    def getYGyroOffsetUser(self):
        pass
        
    def setYGyroOffsetUser(self, value):
        self.i2c.write8(self.MPU6050_RA_YG_OFFS_USRH, value >> 8)
        self.i2c.write8(self.MPU6050_RA_YG_OFFS_USRL, value & 0xFF) 
        return True        
        
    def getZGyroOffsetUser(self):
        pass
        
    def setZGyroOffsetUser(self, value):
        self.i2c.write8(self.MPU6050_RA_ZG_OFFS_USRH, value >> 8)
        self.i2c.write8(self.MPU6050_RA_ZG_OFFS_USRL, value & 0xFF) 
        return True        

    def getIntPLLReadyEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_PLL_RDY_INT_BIT)
     
    def setIntPLLReadyEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_PLL_RDY_INT_BIT, enabled)
     
    def getIntDMPEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_DMP_INT_BIT)
     
    def setIntDMPEnabled(self, enabled):
        self.i2c.writeBit(self.MPU6050_RA_INT_ENABLE, self.MPU6050_INTERRUPT_DMP_INT_BIT, enabled)
        
    def getDMPInt5Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_5_BIT)
        
    def getDMPInt4Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_4_BIT)
        
    def getDMPInt3Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_3_BIT)
        
    def getDMPInt2Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_2_BIT)
        
    def getDMPInt1Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_1_BIT)
        
    def getDMPInt0Status(self):
        return self.i2c.readBit(self.MPU6050_RA_DMP_INT_STATUS, self.MPU6050_DMPINT_0_BIT)
        
    def getIntPLLReadyStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_PLL_RDY_INT_BIT)
        
    def getIntDMPStatus(self):
        return self.i2c.readBit(self.MPU6050_RA_INT_STATUS, self.MPU6050_INTERRUPT_DMP_INT_BIT)
        
    def getDMPEnabled(self):
        return self.i2c.readBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_DMP_EN_BIT)

    def setDMPEnabled(self, status):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_DMP_EN_BIT, status)
    
    def resetDMP(self):
        self.i2c.writeBit(self.MPU6050_RA_USER_CTRL, self.MPU6050_USERCTRL_DMP_RESET_BIT, True)
        
    def setMemoryBank(self, bank, prefetchEnabled = False, userBank = False):
        bank &= 0x1F
        
        if userBank:
            bank |= 0x20
        if prefetchEnabled:
            bank |= 0x40
            
        self.i2c.write8(self.MPU6050_RA_BANK_SEL, bank)
        return True        
        
    def setMemoryStartAddress(self, address):
        self.i2c.write8(self.MPU6050_RA_MEM_START_ADDR, address)       
        
    def readMemoryByte(self):
        result = self.i2c.readU8(self.MPU6050_RA_MEM_R_W)
        return result

    def writeMemoryByte(self, data):
        self.i2c.write8(self.MPU6050_RA_MEM_R_W, data)

    def readMemoryBlock(self):
        pass

    def writeMemoryBlock(self, data, dataSize, bank = 0, address = 0, verify = False):
        self.setMemoryBank(bank)
        self.setMemoryStartAddress(address)
        
        i = 0
        while i < dataSize:  
            self.i2c.write8(self.MPU6050_RA_MEM_R_W, data[i])

            # Verify
            if verify:
                self.setMemoryBank(bank)
                self.setMemoryStartAddress(address)
                result = self.i2c.readU8(self.MPU6050_RA_MEM_R_W)
                
                if result != data[i]:
                    print(data[i]),
                    print(result),
                    print(address)
                    
            # reset adress to 0 after reaching 255
            if address == 255:
                address = 0
                bank += 1

                self.setMemoryBank(bank)
            else:
                address += 1
            
            self.setMemoryStartAddress(address)

            # increase byte index
            i += 1


    def writeDMPConfigurationSet(self, data, dataSize, bank = 0, address = 0, verify = False):
        # config set data is a long string of blocks with the following structure:
        # [bank] [offset] [length] [byte[0], byte[1], ..., byte[length]]
        pos = 0
        while pos < dataSize:
            j = 0
            dmpConfSet = []
            while ((j < 4) or (j < dmpConfSet[2] + 3)):
                dmpConfSet.append(data[pos])
                j += 1
                pos += 1
         
            # write data or perform special action
            if dmpConfSet[2] > 0:
                # regular block of data to write  
                self.writeMemoryBlock(dmpConfSet[3:], dmpConfSet[2], dmpConfSet[0], dmpConfSet[1], verify)
            else:
                # special instruction
                # NOTE: this kind of behavior (what and when to do certain things)
                # is totally undocumented. This code is in here based on observed
                # behavior only, and exactly why (or even whether) it has to be here
                # is anybody's guess for now.
                if dmpConfSet[3] == 0x01:
                    # enable DMP-related interrupts
                    
                    #setIntZeroMotionEnabled(true);
                    #setIntFIFOBufferOverflowEnabled(true);
                    #setIntDMPEnabled(true);
                    self.i2c.write8(self.MPU6050_RA_INT_ENABLE, 0x32);  # single operation  

        
    def getDMPConfig1(self):
        self.i2c.readU8(self.MPU6050_RA_DMP_CFG_1)
        
    def setDMPConfig1(self, config):
        self.i2c.write8(self.MPU6050_RA_DMP_CFG_1, config)        
        
    def getDMPConfig2(self):
        return self.i2c.readU8(self.MPU6050_RA_DMP_CFG_2)

    def setDMPConfig2(self, config):
        self.i2c.write8(self.MPU6050_RA_DMP_CFG_2, config)

    def dmpPacketAvailable(self):
        return self.getFIFOCount() >= self.dmpGetFIFOPacketSize()
    
    def dmpGetFIFOPacketSize(self):
        return self.dmpPacketSize    
    
    def dmpGetAccel(self):
        pass
    
    def dmpGetQuaternion(self, packet):
        # We are dealing with signed bytes
        if packet[0] > 127:
            packet[0] -= 256

        if packet[4] > 127:
            packet[4] -= 256
            
        if packet[8] > 127:
            packet[8] -= 256            
          
        if packet[12] > 127:
            packet[12] -= 256          

        data = {
            'w' : ((packet[0] << 8) + packet[1]) / 16384.0,  
            'x' : ((packet[4] << 8) + packet[5]) / 16384.0,
            'y' : ((packet[8] << 8) + packet[9]) / 16384.0,
            'z' : ((packet[12] << 8) + packet[13]) / 16384.0}        
        
        return data    
    
    def dmpGetGyro(self):
        pass
    
    def dmpGetLinearAccel(self):
        pass
    
    def dmpGetLinearAccelInWorld(self):
        pass
        
    def dmpGetGravity(self, q):
        data = {
            'x' : float(2 * (q['x'] * q['z'] - q['w'] * q['y'])),
            'y' : float(2 * (q['w'] * q['x'] + q['y'] * q['z'])),
            'z' : float(q['w'] * q['w'] - q['x'] * q['x'] - q['y'] * q['y'] + q['z'] * q['z'])}
        
        return data 

    def dmpGetEuler(self, q):
        pass 

    def dmpGetYawPitchRoll(self, q, g):
        data = {
            # yaw: (about Z axis)
            'yaw' : atan2(2 * q['x'] * q['y'] - 2 * q['w'] * q['z'], 2 * q['w'] * q['w'] + 2 * q['x'] * q['x'] - 1),
            # pitch: (nose up/down, about Y axis)
            'pitch' : atan(g['x'] / sqrt(g['y'] * g['y'] + g['z'] * g['z'])),
            # roll: (tilt left/right, about X axis)
            'roll' : atan(g['y'] / sqrt(g['x'] * g['x'] + g['z'] * g['z']))}
            
        return data 

    def dmpProcessFIFOPacket(self):
        pass
        
    def dmpReadAndProcessFIFOPacket(self):
        pass

    def dmpInitialize(self):
        # Resetting MPU6050
        self.reset()
        sleep(0.05) # wait after reset
        
        # Disable sleep mode
        self.setSleepEnabled(False)

        # get MPU hardware revision
        self.setMemoryBank(0x10, True, True) # Selecting user bank 16
        self.setMemoryStartAddress(0x06) # Selecting memory byte 6
        hwRevision = self.readMemoryByte() # Checking hardware revision
        #print('Revision @ user[16][6] ='),
        #print(hex(hwRevision))
        self.setMemoryBank(0, False, False) # Resetting memory bank selection to 0
        
        # get X/Y/Z gyro offsets
        xgOffset = self.getXGyroOffset()
        ygOffset = self.getYGyroOffset()
        zgOffset = self.getZGyroOffset()
        
        # Enable pass through mode
        self.setI2CBypassEnabled(True)
        
        # load DMP code into memory banks
        self.writeMemoryBlock(self.dmpMemory, self.MPU6050_DMP_CODE_SIZE, 0, 0, False)
        #print('Success! DMP code written and verified')
        
        # write DMP configuration
        self.writeDMPConfigurationSet(self.dmpConfig, self.MPU6050_DMP_CONFIG_SIZE, 0, 0, False)
        #print('Success! DMP configuration written and verified')
        
        # Setting clock source to Z Gyro
        self.setClockSource(self.MPU6050_CLOCK_PLL_ZGYRO)
        
        # Setting DMP and FIFO_OFLOW interrupts enabled
        self.setIntEnabled(0x12)
        
        # Setting sample rate to 200Hz
        self.setRate(4) # 1khz / (1 + 4) = 200 Hz [9 = 100 Hz]
        
        # Setting external frame sync to TEMP_OUT_L[0]
        self.setExternalFrameSync(self.MPU6050_EXT_SYNC_TEMP_OUT_L)
        
        # Setting DLPF bandwidth to 42Hz
        self.setDLPFMode(self.MPU6050_DLPF_BW_42)
        
        # Setting gyro sensitivity to +/- 2000 deg/sec
        self.setFullScaleGyroRange(self.MPU6050_GYRO_FS_2000)
        
        # Setting DMP configuration bytes (function unknown)
        self.setDMPConfig1(0x03)
        self.setDMPConfig2(0x00)
        
        # Clearing OTP Bank flag
        self.setOTPBankValid(False)
        
        # Setting X/Y/Z gyro offsets to previous values
        #self.setXGyroOffset(xgOffset);
        #self.setYGyroOffset(ygOffset);
        #self.setZGyroOffset(zgOffset);   
        
        # Setting X/Y/Z gyro user offsets to zero
        self.setXGyroOffsetUser(0)
        self.setYGyroOffsetUser(0)
        self.setZGyroOffsetUser(0)  

        # Writing final memory update 1/7 (function unknown)
        pos = 0
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Writing final memory update 2/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Resetting FIFO
        self.resetFIFO()
        
        # Reading FIFO count
        fifoCount = self.getFIFOCount()
        #print('Current FIFO count = %s' % fifoCount)
        
        # Setting motion detection threshold to 2
        self.setMotionDetectionThreshold(2)
        
        # Setting zero-motion detection threshold to 156
        self.setZeroMotionDetectionThreshold(156)
        
        # Setting motion detection duration to 80
        self.setMotionDetectionDuration(80)
        
        # Setting zero-motion detection duration to 0
        self.setZeroMotionDetectionDuration(0)
        
        # Resetting FIFO
        self.resetFIFO()  

        # Enabling FIFO
        self.setFIFOEnabled(True)
        
        # Enabling DMP
        self.setDMPEnabled(True)
        
        # Resetting DMP
        self.resetDMP()
        
        # Writing final memory update 3/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Writing final memory update 4/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Writing final memory update 5/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Waiting for FIFO count > 2
        while (self.getFIFOCount() < 3):
            fifoCount = self.getFIFOCount()
        #print('Current FIFO count ='),
        #print(fifoCount)
        
        # Reading FIFO data
        self.getFIFOBytes(fifoCount)
        
        # Writing final memory update 6/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)        
       
        # Writing final memory update 7/7 (function unknown)
        j = 0
        dmpUpdate = []
        while ((j < 4) or (j < dmpUpdate[2] + 3)):
            dmpUpdate.append(self.dmpUpdates[pos])
            j += 1
            pos += 1
        
        self.writeMemoryBlock(dmpUpdate[3:], dmpUpdate[2], dmpUpdate[0], dmpUpdate[1], True)
        
        # Disabling DMP (you turn it on later)
        self.setDMPEnabled(False)  
        
        # Setting up internal 42-byte (default) DMP packet buffer
        self.dmpPacketSize = 42
        
        # Resetting FIFO and clearing INT status one last time
        self.resetFIFO()
        self.getIntStatus()