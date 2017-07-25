Launching the webapp.
  commands:
    ./laucher.sh
    sh laucher.sh
  selecting the means of launching the webapp is based on permissions on the local machine.

Accessing the webapp.
  Use URL:
    http://localhost:8080

Using the webapp.
  In the header section of the web page, type desired group name in the search bar.
  If error is displayed then the group name that was entered is unable to be found.
  If webpage comes up displaying Usernames found, then make a selection as to what to do with the User file then select submit located at the bottom of the page.

Output file.
  An output file called decisions.csv will be created/updated with any new User account names not previously in the output file.
  Sorting:
    UserID:GroupID:UserName:DecisionSelected:DeleteUser
