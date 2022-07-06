# Internship
Project for AdataPro Internship</br>
First start Virtual Environment and than install:</br>
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
</br>
<h3>To start The Django site</h3>
<pre>python NLP/main.py</pre>
</br>
<h3>To start The Django site</h3>
<pre>cd internshipProj</pre>
<pre>python manage.py runserver</pre>
go to http://127.0.0.1:8000/

