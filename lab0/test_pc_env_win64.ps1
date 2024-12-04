# conda activate Dora-Camp
#
# dora -V
# python -V
#
# pip3 show torch torchvision torchaudio transformers qwen-vl-utils optimum auto-gptq
#
#
# pause


# 尝试激活conda环境
conda activate Dora-Camp
if ($LastExitCode -ne 0) {
    Write-Output "FAIL"
    pause
    exit
}

# 检查cuda版本
nvcc -V
if ($LastExitCode -ne 0) {
    Write-Output "FAIL"
    pause
    exit
}

# 检查dora版本
dora -V
if ($LastExitCode -ne 0) {
    Write-Output "FAIL"
    pause
    exit
}

# 检查Python版本
python -V
if ($LastExitCode -ne 0) {
    Write-Output "FAIL"
    pause
    exit
}

# 检查pip3包信息
pip3 show torch torchvision torchaudio transformers qwen-vl-utils optimum auto-gptq
if ($LastExitCode -ne 0) {
    Write-Output "FAIL"
    pause
    exit
}

# 如果所有命令都执行成功，则输出pass
Write-Output "PASS"
pause
