# ServoPressKit App

## What is Servo Press Kit

[Servo Press Kit](https://www.festo.com/cms/en-gb_gb/59135.htm) by Festo is a modular press-fitting kit with servo drive 
for electrical press-fitting and joining up to 17 kN.

## App

Web browser app to read the [Servo Press Kit](https://www.festo.com/cms/en-gb_gb/59135.htm) log data. 

Once an individual file is loaded, it plots the Force-Displacement graph from recorded points to analyse press 
scenarios.
Also displays the log file summary with program name, timestamp, result, etc and the source file ‘last modification 
date’ which could indicate the original file was modified.

A single log file is a csv format. Contains all the information related to a press procedure such as the 
press sequence, pass/fail criteria as well as placeholders for unused parameters. App needs to locate and extract all 
the relevant data inside the file in order to proceed. 

<kbd>![](img/sample.gif)</kbd>

### How to use

```
# Clone repository
$ git clone https://github.com/albertkuc/ServoPressKit.git

# Install dependencies
$ pip install -r requirements.txt
```