## <b><font color="red"> notice: </font></b>
##### <b>this readme file is created with atom and uses some special characters that may not be compatible with your readme reader. please use atom to open it or just take a look into the source code.</b>

---

# <b>Directory Contents<b>

The <b><font color="green"> Web_scraper </font></b> directory is the main directory (Github repository also) that you can find the <b><font color="green"> git </font></b> directory inside it to check out the logs. the <b><font color="green"> git </font></b> directory is hidden you can find it by showing the hidden files. 

The <b><font color="green"> WEBSCRAPER </font></b> directory is the main directory that you can find the scripts inside it. We have created some extra files in the <b><font color="green"> WEBSCRAPER </font></b> directory that you can use them and test our application also.

---

# <b> Python Script <b>
## <b> Description <b>

The script <b><font color="orange"> WEBSCRAPER.py </font></b> is the python script which using some std:in (input) method to be run based on your preference.

## <b> Instruction to use the python script

### <b> way 1: using input values by enterring them </b>

Before start the program if you have any html files or list of html files please copy them in the same direcoty as the script directory which is <b><font color="green"> WEBSCRAPER </font></b>.

At first you need to run the python script through your teminal using the command below:

```bash
python3 WEBSCRAPER.py
```

while you enter the mentioned command to run the python script you will face with some options to run the script based on your preference like below:

```
Please specify the type of input method you want to use:

1.a URL or multiple URLs
2.an HTML page or multiple HTML pages
3.a .txt file containing list of HTML pages

Please select one of the above options: [1/2/3]
```


as you can see on the picture you can choose one of the input method.
1.insert one or multiple urls. (such as: https://stallman.org)
2.insert and HTML page or multiple HTML pages (such as: index.html or page2.html)
3.insert a .txt file containing list of HTML pages (such as: listoffile.txt)

if you choose the option #1 the program will ask you to activate the crawling or not which is shown below, and if you choose option #2 or #3 the crawling will be disable during scraping by default:

```
Do you want to keep the CRAWLING Activated? [Y/n]
```

you can pass this step by using the oprions [Y/n] to activate or deactivate the crawling.

in the next step for the urls you need to insert your urls and you can finish the inputting with enterring the <b><font color="yellow"> end </font></b> phrase. and also for the option #2 the program will ask you to enter the HTML file name so you can enter the name and continue the process and as the same for the option #3 you can enter the name of the .txt file containing list of html files to continue.

 ### <b> way 2: piping the values with python script</b>

you can pipe the std:in values within the python script instead of using the script in command prompt format.

in order to work on urls our script needs four or more values 1. url mode ("1"), 2. crawling activate? ("[Y/n]"), 3. url ("url"), 4. input finisher phrase ("end")

the below commands are two examples for the first option:

```bash
(echo "1" && echo "Y" && echo "https://stallman.org" && echo "end" | python3 WEBSCRAPER.py )
```

```bash
(echo "1" && echo "n" && echo "https://stallman.org" && echo "http://swat.polymtl.ca" && echo "end" | python3 WEBSCRAPER.py )
```

in order to work on the html page you just have to pipe two value within the python script. 1. html mode ("2"), 2. html page name ("index.html")

the command below shows the example of mode 2:

```bash
(echo "2" && echo "index.html"| python3 WEBSCRAPER.py )
```
in order to work on the .txt file containing the list of the html pages you can use the same command as previous step except changing the mode to 1. list of file mode ("3") and 2. change the file name to the .txt file ("listoffile.txt")

you can see the example in command below:

```bash
(echo "3" && echo "listoffile.txt"| python3 WEBSCRAPER.py )
```

---

# <b> Bash Script </b>
## <b> Description </b>    
The script <b><font color="orange"> Checker.sh </font></b> can be used to install the node server from git repository with using its url in order to find all the broken links of the project.    

## <b> Instruction to use the bash script </b>
You can run the following command through your terminal thorugh the <b><font color="green"> WEBSCRAPER </font></b> directory.

```bash
./Checker.sh -u < link to github repository > -p < port number to run the server >[optional]    
```

---

#### <b><font color="pink"> We (Dmytro Humeniuk & Mahmood Vahedi) hope you ENJOY </font><b>
