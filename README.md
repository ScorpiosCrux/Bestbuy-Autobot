# Bestbuy Autobuy Bot
- This was a bot created in 2021, it's original purpose was to buy a 30 series Nvidia graphics card from Bestbuy.

## Libraries
- Selenium - This was used to interact with the Bestbuy website.
    - The program will keep refreshing the link until the add to cart button is available. 
    - Once the GPU is added to the cart, the program will checkout and fill out the necessary information.
    - Issues:
        - The constant refreshing fills up your ram and will cause issues after hundreds of refreshes. The solution was to make a separate process that contains the loop, and after a set number of refreshes, it will delete the process, freeing up the memory and it will restart the chrome driver.
- Multiprocessing - Allows us to fix the issue above.