# image-and-annotation-registration
## 适用场景：目标识别中图像标记  
目标识别过程可能会遇到某些图像的整体基本相同，
图像因为扫描的问题发生偏移，
但是需要对其中的某些区域进行标记。这时可以对其中一幅图像进行标记，
然后计算偏移量，并修改标签，
自动对所有图像进行标记。

## 步骤
1. 将同一类型的图像归档至同一文件夹内；
2. 手动标记模版，并确定roi区域，(因为roi区域是固定的，所有只适用于角度旋转较小的图像)
3. 编辑run.bat文件，设置参数；
4. 双击run.bat。

## imreg-dft
[imreg-dft](https://github.com/matejak/imreg_dft)使用离散傅里叶变换实现了图像的校准(registration), 

矢量坐标转换参考了计算机图形学的[知识](https://www.zhihu.com/question/52027040).