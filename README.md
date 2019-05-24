# image-and-annotation-registration
## 适用场景：目标识别中图像标记  
目标识别的数据集制作过程中，可能会遇到某些图像整体基本相同，因为扫描的问题了发生偏移，
但是需要对其中的某些区域进行标记。 
这时可以对其中一幅图像进行标记，
然后计算偏移量，并修改标签，
自动实现对其他图像的标记。

图像的标签按pascal_voc形式进行标记，保存为.xml文件

## 步骤
1. 将同一类型的图像归档至同一文件夹内；
2. 手动标记模版，并确定roi区域，(因为roi区域是固定的，所有只适用于角度旋转较小的图像)
3. 编辑run.bat文件，设置参数；
4. 双击run.bat。

## imreg-dft
[imreg-dft](https://github.com/matejak/imreg_dft)使用离散傅里叶变换实现了图像的校准(registration), 

矢量坐标转换参考了计算机图形学的[知识](https://www.zhihu.com/question/52027040)。


## sift feature
加入sift图像校准方法。