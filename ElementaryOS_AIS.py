#!/usr/bin/python3
# script de instalacion por defecto para elementary OS Freya

clear

echo -e "\e[92mInstalción de de programas despues de instalar Elementary OS Freya"
echo -e "\e[92mActualizando repositorios"
echo -e "\e[0m"
sleep 4s
sudo apt update
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
sudo apt install -y ttf-mscorefonts-installer

echo -e "\e[92m Puedes irte a tomarte un cafe o quedarte mirando pero ya acabo yo solo\e[0m"
sleep 5s;echo -e "\e[92mActualizando el sistema"
echo -e "\e[0m"
sudo apt-get -y upgrade
sudo apt-get -y dist-upgrade

echo -e "\e[92mAñadiendo fuentes de software"
echo -e "\e[0m"
#chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list'

# gimp
sudo add-apt-repository -y ppa:otto-kesselgulasch/gimp
#Elementary tweaks
sudo add-apt-repository -y ppa:mpstark/elementary-tweaks-daily
#synapse no instalo a la espera de que arreglen el icono
#sudo add-apt-repository -y ppa:elementary-os/unstable-upstream


sudo apt update
sudo apt -y upgrade
echo -e "\e[92mInstalando programas"
echo -e "\e[0m"
sudo apt install -y gedit google-chrome-stable ubuntu-restricted-extras gnome-system-tools vlc vlc-plugin-pulse libvlc5 libxine1-ffmpeg gxine mencoder totem-mozilla icedax tagtool easytag id3tool lame  libmad0 mpg321 openshot openshot-doc rar unace p7zip-full unzip p7zip-rar sharutils mpack arj gimp inkscape synaptic gdebi playonlinux calibre libdvdread4 thunderbird libreoffice libreoffice-help-es libreoffice-l10n-es libappindicator1 icedtea-7-plugin openjdk-7-jre terminator elementary-tweaks firefox firefox-locale-es thunderbird thunderbird-locale-es-es brasero build-essential language-pack-gnome-es htop gufw gimp-plugin-registry
# ver dvds
sudo /usr/share/doc/libdvdread4/./install-css.sh
# quitar aplicaciones innecesarias
sudo apt-get remove -y midori-granite geary noise scratch-text-editor
# limpiando paquetes
sudo apt -y autoremove
sudo apt -y autoclean
#Desactivar usuario invitado
echo -e "\e[92mDesactivando sesion de invitado"
echo -e "\e[0m"
sudo echo allow-guest=false >> /usr/share/lightdm/lightdm.conf.d/50-ubuntu.conf
echo -e "\e[92mInstalacion completa"

clear
echo ""
echo -e "\e[1m\e[92mInstalacion completa\e[21m"
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
