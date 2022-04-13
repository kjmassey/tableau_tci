# Tableau Coders Initiative Session #4/5

### Let's start building a Python toolbox using the Tableau Server Client!
---

In this session, we'll start to cover more real-world examples of how you can combine Python and REST API concepts, using the Tableau Server Client (TSC) library for Python. Be sure to check the README in each section for important details about using TSC vs. the REST API based on the scenario. These examples and scenarios will cover some common use cases, but for an exhaustive list of capabilities see:

- [Tableau REST API - All Methods](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref.htm)
- [Tableau Server Client Documentation](https://tableau.github.io/server-client-python/docs/)

## A) Introducing TSC
  - #### What is it? Why use it?
  - #### Installation

## B) Getting/filtering
  - #### Retrieving data, pagination
  - #### Filtering via API vs. Python
  
## C) Looping through actions (automate the boring stuff!)
- #### Refresh multiple extracts from a list of workbooks/datasources
  - Loop through a list of multiple items
  - Get each item from API/TSC
  - Submit refresh request

## D) Publishing a workbook/datasource
- #### TSC wins here, hands down!
- #### Dealing with connections and credentials
  - Sneak peak: Tableau Document API (**TDA**)

## E) Chaining things together -- let's stand up a project!
- #### Create a project on server
- #### Create a server group
- #### Assign permissions to  group
- #### Publish a workbook
