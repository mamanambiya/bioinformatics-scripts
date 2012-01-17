sudo rm /usr/local/mysql
sudo rm -rf /usr/local/mysql*
sudo rm -rf /Library/StartupItems/MySQLCOM
sudo rm -rf /Library/PreferencePanes/My*
rm -rf ~/Library/PreferencePanes/My*
sudo sed -e '/MYSQLCOM=-YES-/d' -e '/MYSQLCOM=-NO-/d' /etc/hostconfig > tmp_file
sudo mv tmp_file /etc/hostconfig
sudo rm -rf /Library/Receipts/mysql*
sudo rm -rf /Library/Receipts/MySQL*
