# Software Requirements Specification  
## For Employee Management System
  
Version 1.0   
Prepared by Bohdan Onsha   
  
10.12.2020  
  
Table of Contents  
=================  
* 1 [Introduction](#1-introduction)  
  * 1.1 [Document Purpose](#11-document-purpose)  
  * 1.2 [Document Conventions](#12-document-conventions)  
  * 1.3 [Intended Audience and Reading Suggestions](#13-intended-audience-and-reading-suggestions)  
  * 1.4 [Project Scope](#14-project-scope)  
* 2 [Overall Description](#2-overall-description)  
  * 2.1 [Product Perspective](#21-product-perspective)  
  * 2.2 [Product Features](#22-product-features)  
  * 2.3 [User Class and Characteristics](#24-user-class-and-characteristics)  
  * 2.4 [Operating Environment](#25-operating-environment)  
* 3 [System Features](#3-system-features)  
  * 3.1 [Description and Priority](#31-description-and-priority)  
  * 3.2 [Stimulus/Response Sequences](#32-stimulus/response-sequence)  
  * 3.3 [Client/Server System](#33-client/server-system)  
* 4 [External Interface Requirements](#4-external-interface-requirements)  
  * 4.1 [User Interfaces](#41-user-interfaces)  
  * 4.2 [Hardware Interfaces](#42-hardware-interfaces)  
  * 4.3 [Software Interfaces](#43-software-interfaces)  
  * 4.4 [Communication Interfaces](#44-communication-interfaces)  
* 5 [Nonfunctional Requirements](#5-nonfunctional-requirements)  
  * 5.1 [Safety Requirements](#51-safety-requirements)  
  * 5.2 [Security Requirements](#52-security-requirements)  


## 1. Introduction  
### 1.1 Document Purpose  
The purpose of this document is to present a detailed description of the Employee Management System. It will explain the purpose and features of the system, the interfaces of the system, what the system will do, the constraints under which it must operate.   
This document is intended for both the stakeholders and the developers of the system.  
  
### 1.2 Document Conventions
This document uses the following conventions.
| Abbreviation | Description    | 
| ---- | ------- |
|   DB     |    Database                           |
|   ER     |    Entity Relationship                |
|   User   |    A person who utilizes the system   |
 
### 1.3 Intended Audience and Reading Suggestions
This project is a prototype for the employee management system and it is restricted within the needs of small and medium-sized businesses. This project is useful for the business managers and as well as the employees.

### 1.4 Project Scope
The purpose of the online employee management system is to ease employee management and to create a convenient and easy-to-use application for managers. The system is based on a relational database. Above all, we hope to provide a comfortable user experience along with easy integration into various business types.

## 2. Overall Description
### 2.1 Product Perspective
A database system stores the following information.
- **Employee details:**
It includes basic information about the employee - name, date of birth, current salary, and the department, where the employee is working on now.
- **Department details:**
It includes basic information about the department - its name and employees data.

### 2.2 Product Features
The major features of the employee management database system as shown in below entity-relationship model (ER model)

![ER diagram](https://i.ibb.co/Zd0SSjh/Screenshot-2020-12-09-at-22-40-46.png)

### 2.3 User Class and Characteristics
Users of the system should be able to retrieve information about the employees and departments of the company they're working in. Users of the system should be able to modify the aforementioned data in the next ways: add new objects, modify existing objects, delete objects of the system.

### 2.4 Operating Environment
The operating environment for the employee management system is as listed below. 

Operating system: **Linux**.
database: **MySql**
platform: **Python**

## 3. System Features
### 3.1 Description and Priority
The employee management system maintains information on employees and departments. Of course, this project has a high priority because it is difficult to maintain a large number of employees without any helping tools.

### 3.2 Stimulus/Response Sequences
- Displays a list of company departments.
- Displays a list of department employees.
- Search for a particular employee with its name and/or date of birth.
- Edit/delete employee data.

### 3.3 Client/Server System
The term client/server refers primarily to an architecture or logical division of responsibilities, the client is the application (also known as the front-end), and the server is the DBMS (also known as the back-end).
A client/server system is a distributed system in which,
    
Some sites are client sites and others are server sites.
All the data resides at the server sites.
All applications execute at the client sites.

## 4. External Interface Requirements
### 4.1 User Interfaces
- Front-end software: **Javascript**
- Back-end software: **Python**

### 4.2 Hardware Interfaces
- **Linux**
- A browser which supports **HTML** and **Javascript**.

### 4.3 Software Interfaces
Following are the software used for the employee management online application.
|    Software user     | Description    |
|        ----          | ------- |
|   Operating system   |    We have chosen Linux operating system for its best support and user-friendliness.     | 
|      Database        |    To save the employee and department records we have chosen MySQL database.     | 
|        Python        |     To implement the project we have chosen Python language for its simplicity and development speed.    | 

### 4.4 Communication Interfaces
This project supports all types of modern web browsers. 

## 5. Nonfunctional Requirements

### 5.1 Safety Requirements
If there is extensive damage to a wide portion of the database due to catastrophic failure, such as a disk crash, the recovery method restores a past copy of the database that was backed up to archival storage (typically tape) and reconstructs a more current state by reapplying or redoing the operations of committed transactions from the backed up log, up to the time of failure.

### 5.2 Security Requirements
Security systems need database storage just like many other applications. However, the special requirements of the security market mean that vendors must choose their database partner carefully.
