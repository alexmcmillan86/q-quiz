===================================================================================================
CS50x FINAL PROJECT by ALEXANDER MCMILLAN
===================================================================================================

PROJECT NAME: Q-Quiz
TYPE: Web Application (Flask)
DATE: 01.09.2020


SITE MAP:
========

Welcome Page
Registration Page
Login Page
Quiz Homepage
Leaderboard Page
Question Pages (x20)


DESCRIPTION:
===========

This is a web application built using Python (Flask), HTML5 & CSS.

On visiting the website, a user is first presented with a welcome page, displaying a brief
description of the site.

On the welcome page, there are two buttons, one for 'register' and the other for 'login'.
New users must register first, as it is required to be logged in to access the quiz homepage.

On the quiz homepage, instructions for the quiz are displayed, as well as a table showing
information specific to the user, such as their name, number of attempts at the quiz and
also their first score and most recent score from the quiz. Below the table are also two
buttons, one for redirecting to the leaderboard page and the other for starting the quiz.

When the user selects the 'start quiz!' button, the first question with multiple choice
answers is displayed. There are 20 questions in total for the quiz and each question page
displays four multiple choice answers to the user, which are randomly sorted each time the
quiz is generated. Some questions also include an image.

An answer is selected by clicking the button on which the answer text is displayed. When this
occurs, the background colour of the button will turn pink to show it has been selected and
then the next question will be automatically loaded. If the correct answer has been choosen,
then in the database 'quiz.db' a table titled 'users' is updated with the running score.
For a correct answer the user has 100 points added to their score, if any incorrect answer is
given, then the running score remains unchanged.

When the final question is answered, the leaderboard is displayed and the user can see their
position relative to others who have taken the quiz. The data displayed on the leaderboard
is ordered by descending score and in case of a tie, in descending datetime. At the bottom of
the leaderboard page, there is a button to return to the quiz homepage.

An attempt at the quiz is only recorded once the final question has been answered.
At all times while the user is logged in, a logout link in the navigation bar is displayed and
active. When the user has successfully logged out they are taken back to the login page.

On every page of the website a footer is displayed, with copyright information and also
a link to CS50x on edX.


DATABASE:
========

TITLE: quiz.db
TABLES: users, leaderboard, answers


LINKS:
=====

Live Demo:
YouTube Project Overview:


ACKNOWLEDGEMENTS:
===============

Special thanks to David Malan, Brian Yu, Doug Lloyd and all the staff at CS50.