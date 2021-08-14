# 实现目标

基于 Pandoc 来实现 Markdown 和 Html 到电子书的转换

1. 能够支持 Markdown 转换为 Epub 和 PDF 两种格式;
2. 能够支持 Html 转换为 Epub 和 PDF 两种格式

# 脚本设计

输入参数：

```shell
-f 输入的文本格式
-t 输出文本格式
-i --input 输入文件或者目录
-o 输出文件
```


# reference

1. [wordshub/free-font: 大概是2020年最全的免费可商用字体，这里收录的商免字体都能找到明确的授权出处，可以放心使用，持续更新中...](https://github.com/wordshub/free-font)
2. [Converting Markdown to Beautiful PDF with Pandoc - jdhao's blog](https://jdhao.github.io/2019/05/30/markdown2pdf_pandoc/)