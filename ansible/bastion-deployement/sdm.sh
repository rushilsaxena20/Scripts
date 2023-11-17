#!/bin/bash
export SDM_ADMIN_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODA2MTI0MjgsIm9yZ2FuaXphdGlvbklkIjoxMzYxLCJjcmVhdG9yIjoicHVsa2l0QG1vZW5nYWdlLmNvbSIsImNyZWF0b3JJZCI6MTU0MjQ1ODQwMTI4NDk2NDUyOCwiZ3VpZCI6IjEwNzVjZTRmLTU3OGYtNDM2My1hZTI0LTQ3YzJiOTk3NGY0YyIsIm5hbWUiOiJzZG0tYW5zaWJsZSJ9.mTCrzGqQOObWXCFZ3_hBk1CLI-hXS5mAnCzGncqr5gQ

echo TARGET_USER="$1"

sudo apt update
sudo apt install -y unzip

instance_id=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
region=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)

curl -o sdm.zip -L https://app.strongdm.com/releases/cli/linux
unzip sdm.zip
sudo cp sdm /usr/local/bin/ 
 
sdm admin ssh add    --tags "Business=bastion-$1"    -p Data-Bastion    $TARGET_USER@`curl http://169.254.169.254/latest/meta-data/hostname`    | sudo tee -a "/home/$TARGET_USER/.ssh/authorized_keys" 
rm sdm.zip