#!/usr/bin/python3
#instalacion por defecto
clear
echo "Instalción de de programas despues de instalar Ubuntu 14.04 trusty tahr"
echo "Actualizando repositorios"
sudo apt-get update
echo -e "\e[92mAhora instalamos las fuentes de windows ya que es el unico paquete que pide interactuar"
echo -e "\e[0m"
echo -e "\e[93mInstrucciones"
echo -e "\e[0m"
echo -e "1) \e[93mPulsa la \e[0m\e[4mflecha de la derecha\e[24m\e[93m  y luego \e[0m\e[4mEnter\e[24m \e[93m cuando \e[0m\e[41mAceptar\e[0m\e[93m este en Rojo\e[0m"
echo -e "2) \e[93mSelecciona \e[0m\e[4mSI\e[24m\e[93m y luego pulsa \e[0m\e[4mEnter\e[24m\e[0m"
echo -e "3) \e[93mY ya puedes dejar el ordenador solo hasta que termine\e[0m"
echo -e ""
echo -e ""
echo -e "\e[92m Pulsa enter cuando lo hayas entendido\e[0m"
read $A
sudo apt-get install -y ttf-mscorefonts-installer

echo -e "\e[92m Puedes irte a tomarte un cafe o quedarte mirando pero ya acabo yo solo\e[0m"
sleep 5s;echo -e "\e[92mActualizando el sistema"
echo -e "\e[0m"

sudo apt-get -y upgrade
#chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list'
echo "Añadiendo fuentes de software"

#gimp
sudo add-apt-repository -y ppa:otto-kesselgulasch/gimp
#myweather indicator
sudo add-apt-repository -y ppa:atareao/atareao



sudo apt-get update
sudo apt-get -y upgrade
echo "Instalando programas"
sudo apt-get install -y google-chrome-stable ubuntu-restricted-extras vlc vlc-plugin-pulse libvlc5 libxine1-ffmpeg mencoder lame libmad0 mpg321 openshot openshot-doc rar unace p7zip-full unzip p7zip-rar sharutils mpack arj gimp synaptic libavcodec-extra calibre libdvdread4 libreoffice-help-es libreoffice-l10n-es  libappindicator1 icedtea-7-plugin openjdk-7-jre terminator gimp-plugin-registry x264 preload prelink myspell-es gparted cabextract file-roller uudeview my-weather-indicator lm-sensors laptop-mode-tools gparted gedit gedit-plugins gnome-system-monitor
# Desactivar notificaciones de informe de error
sudo sed -i s/enabled=1/enabled=0/g /etc/default/apport
# ver dvds
sudo /usr/share/doc/libdvdread4/./install-css.sh

# limpiando paquetes
sudo apt-get -y autoremove
sudo apt-get -y autoclean

clear
echo ""
echo -e "\e[1m\e[92mInstalacion completa\e[21m"
echo ""
echo ""
# Mensaje de despedida
echo ""
echo ""
echo ""
sleep 1s;echo -e "\e[92mNo olvides visitarnos en"
echo ""
echo ""
sleep 1s;echo -e "\e[42m\e[91m*****************************************************************"
sleep 1s;echo -e "\e[93m+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
sleep 1s;echo -e "            \e[42m   \e[97m\e[1mhttp://aplicacionesysistemas.com\e[21m                  \e[0m"
sleep 1s;echo -e "\e[42m\e[93m+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\e[0m"
sleep 1s;echo -e "\e[42m\e[91m*****************************************************************\e[0m"
echo ""
# Para que pregunte si queremos reiniciar
echo -e "\e[91m¿Quieres reiniciar? (S/n)\e[0m"
read D

if [[ "$D" == "n" ]];
then
    echo -e "\e[42m\e[97m\e[1mGracias por utilizar mi script\e[0m"
else
    sleep 4s;echo -e "\e[42m\e[97m\e[1mReiniciando\e[0m"
    sudo sleep 1s;shutdown -r +0
