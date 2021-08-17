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

# 容器中包含了 XeLaTeX 语法配置

通常，文稿由两部分构成，一部分是正文内容，另一部分是排版控制语句。下面主要说下 xelatex 下的控制语句。控制语句的格式如下:

```latex
\命令名[可省略的参数]{不可省略的参数}
```

对配置中对属性设置进行说明

1. 如果是中文字符，则最好应用中文的断行规则，否则会出现右边字符超出边界的情况。

```latex
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt
```

上述指令中，`\XeTeXlinebreaklocale` 指定使用中文断行规则，`\XeTeXlinebreakskip` 可以 让 `XeLaTeX` 处理中文断行时多一点点自适应调整的空间。

2. 设置纸张大小

通常设置，在一张 A4 纸上以 11pt 为基本字体尺寸， 也可以设置排版方向。
```latex
\documentclass[a4paper,11pt]{article}
```

3. 设置页面边距

```latex
\usepackage[top=1in,bottom=1in,left=1.25in,right=1.25in]{geometry}
```

# reference

1. [wordshub/free-font: 大概是2020年最全的免费可商用字体，这里收录的商免字体都能找到明确的授权出处，可以放心使用，持续更新中...](https://github.com/wordshub/free-font)
2. [Converting Markdown to Beautiful PDF with Pandoc - jdhao's blog](https://jdhao.github.io/2019/05/30/markdown2pdf_pandoc/)
3. [CTAN: /tex-archive/language/chinese/ctex](https://www.ctan.org/tex-archive/language/chinese/ctex)