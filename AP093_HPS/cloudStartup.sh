cd ~
apt update
$(git clone https://github.com/intel-iot-devkit/terasic-de10-nano-kit.git)

cd /home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule

$(python3.7 -m pip install -r ./requirements.txt)


overlay_dir="/sys/kernel/config/device-tree/overlays/socfpga_1"
overlay_dtbo="rfs-overlay.dtbo"
overlay_rbf="Module5_Sample_HW.rbf"

if [ -d $overlay_dir ];then
    rmdir $overlay_dir
fi

rm -r AP093HPS

$(git clone https://github.com/g00g1y5p4/AP093HPS.git)


cd "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/overlay/"

cp $overlay_dtbo /lib/firmware/
cp $overlay_rbf /lib/firmware/

mkdir $overlay_dir


#echo "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/overlay/rfs-overlay.dtbo" > $overlay_dir/path

cd "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/"

cp AP093HPS/* ./

echo "https://innovatefpga-portal-fpgadesign.azurewebsites.net/"

$(python3.7 -u /home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/main.py)

