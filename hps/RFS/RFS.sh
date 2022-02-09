cd 
cd intelFPGA_lite/21.1/quartus/bin/
./quartus_pgm -c 1 -m jtag -o "p;/home/g00g1y5p4/Documents/de10_nano/RFS/RFS/DE10_Nano_WiFi_Network_Time/demo_batch/WiFi_Network_Time.sof
@2"
cd
cd /home/g00g1y5p4/Documents/de10_nano/RFS/RFS/DE10_Nano_WiFi_Network_Time/demo_batch/
sh /home/g00g1y5p4/intelFPGA_lite/21.1/nios2eds/nios2_command_shell.sh /home/g00g1y5p4/intelFPGA_lite/21.1/nios2eds/bin/nios2-download WiFi_Network_Time.elf -c 1 -r -g
sh /home/g00g1y5p4/intelFPGA_lite/21.1/nios2eds/nios2_command_shell.sh /home/g00g1y5p4/intelFPGA_lite/21.1/quartus/bin/nios2-terminal -c 1
