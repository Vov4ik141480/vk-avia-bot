log_config = {
    "version": 1,
    "formatters": {
        "main_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s in %(filename)s - %(funcName)s: %(message)s" 
        }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "main_formatter",
            "filename": "logs.log",
            "maxBytes": 512000,
            "backupCount": 0,
            "encoding": "UTF-8"        
        }
    },
    "loggers": {
        "main": {
            "handlers": ["file"],
            "level": "DEBUG"
        },
    }

}
