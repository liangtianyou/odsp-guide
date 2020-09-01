########################################
smartctl - 硬盘监控和分析工具
########################################

`原文 - 硬盘监控和分析工具：smartctl <https://linux.cn/article-4682-1.html>`_

``smartctl`` （ **S.M.A.R.T** 自监控，分析和报告技术）是类 Unix 系统下实施 **S.M.A.R.T** 任务命令行套件或工具，它用于打印 **S.M.A.R.T** 自检和错误日志，启用并禁用 **S.M.A.R.T** 自动检测，以及初始化设备自检。

``smartctl`` 对于 **Linux** 物理服务器十分有用，在这些服务器上，可以对智能磁盘进行错误检查，并将与硬件RAID相关的磁盘信息摘录下来。

在本帖中，我们将讨论 ``smartctl`` 命令的一些实用样例。如果你的 Linux 上还没有安装 ``smartctl``，请按以下步骤来安装。

.. image:: /media/disk/smart/smart_01.png
   :align: center

安装 smartctl
~~~~~~~~~~~~~~~~~~~~~~~~~~
对于 Ubuntu

.. code-block:: sh
    :linenos:
    
    $ apt-get install smartmontools

对于 CentOS & RHEL

.. code-block:: sh
    :linenos:

    # yum install smartmontools

启动smartctl服务
~~~~~~~~~~~~~~~~~~~~~~~~~~

对于 Ubuntu

.. code-block:: sh
    :linenos:
    
    $ /etc/init.d/smartmontools start
    
    $ systemctl start smartmontools && systemctl enable smartmontools

对于 CentOS & RHEL

.. code-block:: sh
    :linenos:

    # service smartd start ; chkconfig smartd on
    
    # systemctl start smartd && systemctl enable smartd

样例
~~~~~~~~~~~~~~~~~~~~~~~~~~
样例1 检查磁盘的 Smart 功能是否启用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -i /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF INFORMATION SECTION ===
    Model Family:     Seagate Momentus 5400.6
    Device Model:     ST9320325AS
    Serial Number:    5VD2V59T
    LU WWN Device Id: 5 000c50 020a37ec4
    Firmware Version: 0002BSM1
    User Capacity:    320,072,933,376 bytes [320 GB]
    Sector Size:      512 bytes logical/physical
    Rotation Rate:    5400 rpm
    Device is:        In smartctl database [for details use: -P show]
    ATA Version is:   ATA8-ACS T13/1699-D revision 4
    SATA Version is:  SATA 2.6, 1.5 Gb/s
    Local Time is:    Sun Nov 16 12:32:09 2014 IST
    SMART support is: Available - device has SMART capability.
    SMART support is: Enabled

这里 **/dev/sdb** 是你的硬盘。上面输出中的最后两行显示了 **S.M.A.R.T** 功能已启用。

样例2 启用磁盘的 **S.M.A.R.T** 功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -s on /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF ENABLE/DISABLE COMMANDS SECTION ===
    SMART Enabled.

样例3 禁用磁盘的 **S.M.A.R.T** 功能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -s off  /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF ENABLE/DISABLE COMMANDS SECTION ===
    SMART Disabled. Use option -s with argument 'on' to enable it.

样例4 显示磁盘的详细 **S.M.A.R.T** 信息
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -a /dev/sdb              // For IDE drive
    root@linuxtechi:~# smartctl -a -d ata /dev/sdb       // For SATA drive

样例5 显示磁盘总体健康状况
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -H  /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF READ SMART DATA SECTION ===
    SMART overall-health self-assessment test result: PASSED
    Warning: This result is based on an Attribute check.
    Please note the following marginal Attributes:
    ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
    190 Airflow_Temperature_Cel 0x0022   067   045   045    Old_age   Always   In_the_past 33 (Min/Max 25/33)

样例6 使用long和short选项测试硬盘
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Long测试

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl --test=long /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF OFFLINE IMMEDIATE AND SELF-TEST SECTION ===
    Sending command: "Execute SMART Extended self-test routine immediately in off-line mode".
    Drive command "Execute SMART Extended self-test routine immediately in off-line mode" successful.
    Testing has begun.
    Please wait 102 minutes for test to complete.
    Test will complete after Sun Nov 16 14:29:43 2014
     
    Use smartctl -X to abort test.

或者，我们可以重定向测试输出到日志文件，就像下面这样

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl --test=long /dev/sdb > /var/log/long.text

Short测试

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl --test=short /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF OFFLINE IMMEDIATE AND SELF-TEST SECTION ===
    Sending command: "Execute SMART Short self-test routine immediately in off-line mode".
    Drive command "Execute SMART Short self-test routine immediately in off-line mode" successful.
    Testing has begun.
    Please wait 1 minutes for test to complete.
    Test will complete after Sun Nov 16 12:51:45 2014
     
    Use smartctl -X to abort test.

或

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl --test=short /dev/sdb > /var/log/short.text

注意：short测试将花费最多2分钟，而在long测试中没有时间限制，因为它会读取并验证磁盘的每个段。

样例7 查看驱动器的自检结果
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -l selftest /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF READ SMART DATA SECTION ===
    SMART Self-test log structure revision number 1
    Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
    # 1  Short offline       Completed: read failure       90%       492         210841222
    # 2  Extended offline    Completed: read failure       90%       492         210841222

样例8 计算测试时间估值
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -c  /dev/sdb
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF READ SMART DATA SECTION ===
    General SMART Values:
    Offline data collection status:  (0x00)    Offline data collection activity
                        was never started.
                        Auto Offline Data Collection: Disabled.
    Self-test execution status:      ( 121)    The previous self-test completed having
                        the read element of the test failed.
    Total time to complete Offline 
    data collection:         (    0) seconds.
    Offline data collection
    capabilities:              (0x73) SMART execute Offline immediate.
                        Auto Offline data collection on/off support.
                        Suspend Offline collection upon new
                        command.
                        No Offline surface scan supported.
                        Self-test supported.
                        Conveyance Self-test supported.
                        Selective Self-test supported.
    SMART capabilities:            (0x0003)    Saves SMART data before entering
                        power-saving mode.
                        Supports SMART auto save timer.
    Error logging capability:        (0x01)    Error logging supported.
                        General Purpose Logging supported.
    Short self-test routine 
    recommended polling time:      (   1) minutes.
    Extended self-test routine
    recommended polling time:      ( 102) minutes.
    Conveyance self-test routine
    recommended polling time:      (   2) minutes.
    SCT capabilities:            (0x103b)    SCT Status supported.
                        SCT Error Recovery Control supported.
                        SCT Feature Control supported.
                        SCT Data Table supported.

样例9 显示磁盘错误日志
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh
    :linenos:

    root@linuxtechi:~# smartctl -l error  /dev/sdb
     
    Sample Output
     
    smartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.13.0-32-generic] (local build)
    Copyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org
     
    === START OF READ SMART DATA SECTION ===
    SMART Error Log Version: 1
    ATA Error Count: 5
        CR = Command Register [HEX]
        FR = Features Register [HEX]
        SC = Sector Count Register [HEX]
        SN = Sector Number Register [HEX]
        CL = Cylinder Low Register [HEX]
        CH = Cylinder High Register [HEX]
        DH = Device/Head Register [HEX]
        DC = Device Command Register [HEX]
        ER = Error register [HEX]
        ST = Status register [HEX]
    Powered_Up_Time is measured from power on, and printed as
    DDd+hh:mm:SS.sss where DD=days, hh=hours, mm=minutes,
    SS=sec, and sss=millisec. It "wraps" after 49.710 days.
     
    Commands leading to the command that caused the error were:
      CR FR SC SN CL CH DH DC   Powered_Up_Time  Command/Feature_Name
      -- -- -- -- -- -- -- --  ----------------  --------------------
      25 da 08 e7 e5 a5 4c 00      00:30:44.515  READ DMA EXT
      25 da 08 df e5 a5 4c 00      00:30:44.514  READ DMA EXT
      25 da 80 5f e5 a5 4c 00      00:30:44.502  READ DMA EXT
      25 da f0 5f e6 a5 4c 00      00:30:44.496  READ DMA EXT
      25 da 10 4f e6 a5 4c 00      00:30:44.383  READ DMA EXT
