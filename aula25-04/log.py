import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    
)
def log_info(menssage):
    logging.info(menssage)
    
    
def log_error(menssagem):
    logging.error(message)
    
