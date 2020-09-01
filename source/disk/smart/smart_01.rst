################################
SMART - 磁盘监控方案
################################
`原文地址 - SMART 磁盘监控方案 <https://www.yisu.com/zixun/113438.html>`_

命令行使用说明
~~~~~~~~~~~~~~~~~~~~~~
目前我们使用的服务器都带有lsi的raid卡，当磁盘为SAS盘时使用smartctl时需要添加：

.. code-block:: sh
    :linenos:
    
    smartctl -d megaraid,$deviceid /dev/$diskname

当磁盘为SATA盘时使用smartctl时需要添加：

.. code-block:: sh
    :linenos:
    
    smartctl -d sat+megaraid,$deviceid /dev/$diskname

可以使用raid卡工具来查看磁盘接口类型

.. code-block:: sh
    :linenos:

    megacli -cfgdsply -aall |grep 'PD TYPE'


命令行返回值
~~~~~~~~~~~~~~~~~~~~~~
``smartctl`` 执行完毕之后可以从 **shell** 变量 ``$?`` 中取得返回值，如果磁盘完全正常则返回值为 **0**，否则根据错误类型设置相应的bit位。

bit位说明如下:
    * Bit 0: Command line did not parse.
    * Bit 1: Device open failed， device did not return an IDENTIFY DEVICE structure， or device is in a low-power mode (see -n option above).
    * Bit 2: Some SMART or other ATA command to the disk failed， or there was a checksum error in a SMART data structure (see -b option above).
    * Bit 3: SMART status check returned "DISK FAILING".
    * Bit 4: We found prefail Attributes <= threshold.
    * Bit 5: SMART status check returned "DISK OK" but we found that some (usage or prefail) Attributes have been <= threshold at some time in the past.
    * Bit 6: The device error log contains records of errors.
    * Bit 7: The device self-test log contains records of errors.  [ATA only] Failed self-tests outdated by a newer successful extended self-test are ignored.

查看bit设置:
    .. code-block:: sh
        :linenos:
        
        status=$?
        for ((i=0; i<8; i++)); do
            echo "Bit $i: $((status & 2**i && 1))" 
        done

需要重点监控 **bit3， bit4， bit6， bit7， bit5** 是否设置，其他位置的设置需要提醒。

``smartctl`` 显示的属性(Attribute)信息:

以公司内的一台服务器为例说明:

    .. code-block:: sh
        :linenos:
        
        [root@datacenter1.rack1.node11 ~]#smartctl -A -P use /dev/sdb
        smartctl 5.42 2011-10-20 r3458 [x86_64-linux-2.6.32-279.el6.x86_64] (local build)
        Copyright (C) 2002-11 by Bruce Allen， http://smartmontools.sourceforge.net

        === START OF READ SMART DATA SECTION ===
        SMART Attributes Data Structure revision number: 16
        Vendor Specific SMART Attributes with Thresholds:
        ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
          1 Raw_Read_Error_Rate     0x000b   086   086   016    Pre-fail  Always       -       10813449
          2 Throughput_Performance  0x0005   132   132   054    Pre-fail  Offline      -       105
          3 Spin_Up_Time            0x0007   117   117   024    Pre-fail  Always       -       615 (Average 615)
          4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       314
          5 Reallocated_Sector_Ct   0x0033   100   100   005    Pre-fail  Always       -       0
          7 Seek_Error_Rate         0x000b   100   100   067    Pre-fail  Always       -       0
          8 Seek_Time_Performance   0x0005   112   112   020    Pre-fail  Offline      -       39
          9 Power_On_Hours          0x0012   097   097   000    Old_age   Always       -       23637
         10 Spin_Retry_Count        0x0013   100   100   060    Pre-fail  Always       -       0
         12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       313
        192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       478
        193 Load_Cycle_Count        0x0012   100   100   000    Old_age   Always       -       478
        194 Temperature_Celsius     0x0002   222   222   000    Old_age   Always       -       27 (Min/Max 5/70)
        196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
        197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
        198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
        199 UDMA_CRC_Error_Count    0x000a   200   200   000    Old_age   Always       -       0

1. 首先不同的磁盘厂商提供的 **ATTRIBUTE_NAME** 列表可能不一样，只是 **S.M.A.R.T** 属性列表的子集，**S.M.A.R.T** 完整的属性列表及其每个属性的含义请参考这里:

    `<http://en.wikipedia.org/wiki/S.M.A.R.T.#8>`_

2. 我们需要关注的字段 WHEN_FAILED
    WHEN_FAILED字段显示的规则:
    
    .. code-block:: sh
        :linenos:

        if(VALUE <= THRESH)
            WHEN_FAILED ＝ "FAILING_NOW";
        else if (WORST <= THRESH)
            WHEN_FAILED ＝ "in_the_past"(or past);
        else 
            WHEN_FAILED ＝ "-";

也就说当某个 **ATTRIBUTE_NAME** 的 **WHEN_FAILED** 字段为 **-** 时表示这个属性是正常的，也从没发生过异常。

同时当 ``smartctl`` 命令的返回值的 **bit4，bit5** 设置就可以检查看哪个 **ATTRIBUTE_NAME** 为非 **-** 就表示这个字段出问题了。

简单的smartctl监控方案
~~~~~~~~~~~~~~~~~~~~~~~~~~~
针对每块盘没半个小时执行一次 ``smartctl`` 扫描:

.. code-block:: sh
    :linenos:
    
    smartctl -a  /dev/$devname

每次都要检查 ``smartctl`` 的返回值，如果返回值的 **bit2**，可以使用 ``smartctl -x -b warn /dev/$devname`` 可以看到不支持哪些命令。

.. code-block:: sh
    :linenos:
    
    Warning: device does not support SCT Data Table command
    Warning: device does not support SCT Error Recovery Control command
    
如果返回值的 **bit4** 或者 **bit5** 设置，则需要检查 ``smartctl`` 输出中的 **START OF READ SMART DATA SECTION**，即上节所讲的 **ATTRIBUTE**，并记录 **WHEN_FAILED** 字段非 **-** 的 **ATTRIBUTE_NAME**。

如果返回值的 **bit6** 设置，记录 ``smartctl -l xerror /dev/$devname`` 的执行结果。

如果返回值的 **bit7** 设置，记录 ``smartctl -l xselftest /dev/$devname`` 的执行结果。

如果 **bit3** 设置表示 **S.M.A.R.T** 自检失败.

以上的 **bit** 除了 **bit5**，其他最好都能实时的发出警报信息，其他 **bit** 如果置位，可以不需要实时的警报。

针对ATTRIBUTE_NAME的一些说明
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
由于不同厂商的磁盘提供的 **ATTRIBUTE_NAME** 不完全一致，加上我现在对某些字段的含义理解不够，所以警报信息暂时不按照 **ATTRIBUTE_NAME** 来区分。

比如我们比较关注的 **Throughput_Performance**，公司内的日立的磁盘的 **S.M.A.R.T** 包含有此信息，而希捷的盘没有。

至于需要更细化的监控方案需要对 **ATTRIBUTE_NAME** 中的属性有深入的理解再做定夺。

ssd盘的寿命监控
~~~~~~~~~~~~~~~~~~~~~~~
ssd 盘的寿命监控主要监控以下的 **ATTRIBUTE**:
    * Media_Wearout_Indicator:    使用耗费， 表示SSD上NAND的擦写次数的程度
    * Reallocated_Sector_Ct:      出厂后产生的坏块个数
    * Host_Writes_32MiB:          已写32MiB的个数.
    * Available_Reservd_Space:    SSD上剩余的保留空间。

以上的 **ATTRIBUTE** 只要 **VALUE** 字段接近 **THRESH** 字段的值就需要报警，同样可以使用上边的说明来处理。
