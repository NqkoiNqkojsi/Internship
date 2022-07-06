# Internship
<h3>Dependecies</h3>
Project for AdataPro Internship</br>
First start Virtual Environment and then install:</br>
<pre>pip install scrapy</pre>
<pre>pip install peewee</pre>
<pre>pip install scrapy_jsonschema</pre>
<pre>pip install django</pre>
<pre>pip install classla</pre>
</br>
<h3>To start Crawler</h3>
To run the spiders generating the databases:</br>
<pre>python GovScraper/start.py</pre>
This code will run 3 spiders:</br>
First to generate the urls for all the articles in a links.db</br>
Second to generate articles.db with all the necessary information from the articles</br>
<h3>Set up the deployment environment</h3>
<h5>AWS</h5>
First, go to https://aws.amazon.com/ and create a free-tier account.
Then, choose the EC2 service.
After that, you have to pick on what OS the server will run. Choose Debian-11.
Then you get the option to configure the specs of the server through the 'instance-type'. We chose t2-micro.
<h5>SSH Access</h5>
To configure the SSH access to the cloud we used PuTTY. It can be downloaded from https://www.putty.org/.
From here on we have to configure the PuTTY with the .pem key we get from AWS.
<h5>Installing packages</h5>
You can install the packages you need with debian commands through the shell.
</br>
<h3>To start The Django site</h3>
<pre>cd internshipProj</pre>
<pre>python manage.py runserver</pre>
Lastly, go to http://127.0.0.1:8000/

