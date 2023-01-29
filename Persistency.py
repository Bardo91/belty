#
# PatPab Corporation 
# The coolest company to be in
#

from pathlib import Path
import os

# This class provides for root directories to store the databases, and 
# configuration files.
class Persistency:
    def defaultDir(self) -> str:
        return str(Path.home())+"/patpab"
    
    def checkFileExist(self, path : str) -> bool:
        return os.path.exists(path)

    def createDirs(self, path: str) -> None:
        os.makedirs(path)
    
    