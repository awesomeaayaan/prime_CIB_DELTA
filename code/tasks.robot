*** Settings ***
Documentation     Template robot main suite.
Library           Bot.py
Library           WeightageProcess.py
Task Teardown     Teardown

*** Tasks ***
RPA Task
    Start