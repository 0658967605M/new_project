# Django News Publishing Platform

A role-based News Publishing Web Application built with Django and MySQL.
This platform allows journalists to create articles, editors to approve them, and readers to read and subscribe to their favorite journalists and publishers.

# Poject Overview
This project demonstrates:
Custom user roles
Role-based permissions
Article publishing workflow
Subscription system (follow/unfollow)
Clean Django architecture
Template inheritance
Relational database design
It is built as a full-stack backend + template-based web application using Django.

## User Roles & Capabilities
# Reader
View approved articles
Read full article details
Subscribe to journalists
Subscribe to publishers
Unsubscribe anytime
See dynamic Subscribe / Unsubscribe buttons

# Journalist
Create new articles
Edit own articles
Delete own articles
Assign publisher to article
View own article list
Articles created by journalists require editor approval before being visible to readers.

# Editor
View unapproved articles
Approve articles
Manage publishing workflow

## Features
# Authentication
Custom user model
Login / Register
Role selection during registration
Login required for dashboard access

# Article Management
Create Article
Update Article
Delete Article
Read Article
Approval system
Timestamp (created_at)
Publisher association

# Subscription System
Subscribe to Journalist
Subscribe to Publisher
Prevent duplicate subscriptions
Unsubscribe feature
Dynamic UI buttons
Role-based restriction (only readers can subscribe)

# Dashboard System
Dashboard content changes based on role:
Reader Dashboard → Shows approved articles + subscribe buttons
Journalist Dashboard → Shows own created articles
Editor Dashboard → Shows pending articles for approval

## Database Models
# User
username
password
role (reader / journalist / editor)
publisher_profile (optional, for journalists)

# Article
title
content
created_by (User)
publisher (Publisher)
approved (Boolean)
created_at (DateTime)

# Publisher
name
description

# Subscription
reader (User)
journalist (User, nullable)
publisher (Publisher, nullable)
created_at
Unique constraints to prevent duplicates