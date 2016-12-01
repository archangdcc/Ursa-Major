Build
---------------------
* web-ui:

    Requirement:

    ```
    sudo apt-get install npm
    sudo ln -s /usr/bin/nodejs /usr/bin/node
    sudo npm install -g grunt-cli jshint

    ```

    Build:

    ```
    npm install
    grunt prereq
    grunt build
    ```
