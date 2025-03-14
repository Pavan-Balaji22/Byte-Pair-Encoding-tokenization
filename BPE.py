import regex as re
class BPETokenizer:
    def __init__(self, nmerges: int):
        self.nextByte: int= 256
        self.nmerges: int = nmerges
        pass
    
    def _get_counts(self,byteData:list):
        counts = {}
        for i,j in zip(byteData,byteData[1:]):
            counts[i,j]=counts.get((i,j),0)+1
        return counts

    def _do_merges(self,keys:tuple,token:int,byteData: list) -> list:
        i=0
        while i < (len(byteData)-1):
            i+=1
            if byteData[i] == keys[0] and byteData[i+1] == keys[1]:
                byteData[i] = token
                byteData.pop(i+1)
                i+=1
        return byteData
    
    def train(self,text:str):
        self.bytesData = [x for x in text.encode(errors="replace")]
        self.merges_dict: dict = {}
        for x in range(self.nmerges):
            bp_counts = self._get_counts(self.bytesData)
            req_key = max(bp_counts.items(),key=lambda x:x[1])[0]
            self.merges_dict[req_key] = self.nextByte + x
            self.bytesData = self._do_merges(req_key,self.nextByte+x,self.bytesData)
        
        self.decode_dict = {v:k for k,v in self.merges_dict.items()}
        

    def encode(self,text:str) -> list:
        tokens = [x for x in text.encode(errors="replace")]
        i=0
        while i < (len(tokens)-1):
            
            if self.merges_dict.get((tokens[i],tokens[i+1]),False):
                tokens[i] = self.merges_dict[(tokens[i],tokens[i+1])]
                tokens.pop(i+1)
                i+=1
            else:
                i+=1
        
        return tokens
                

    def decode(self,tokens:list) -> str:
        bytes = []
        i=0
        while i < (len(tokens)):
            
            if self.decode_dict.get(tokens[i],False):
                bytes.extend(self.decode_dict[tokens[i]])
                i+=1
            else:
                bytes.extend([tokens[i]])
                i+=1
        return "".join([chr(x) for x in bytes])