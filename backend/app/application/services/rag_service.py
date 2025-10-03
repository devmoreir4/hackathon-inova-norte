import os
import glob
from typing import List, Dict, Any
from openai import OpenAI

class RAGService:
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required."
            )
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.knowledge_base = {}
        self.data_folder = "data/documents"
        self.files_timestamp = 0
        
        system_prompt = os.getenv("RAG_SYSTEM_PROMPT")
        if not system_prompt:
            raise ValueError(
                "RAG_SYSTEM_PROMPT environment variable is required. "
            )
        self.system_prompt = system_prompt

    def _has_new_files(self) -> bool:
        if not os.path.exists(self.data_folder):
            return False
            
        patterns = [
            f"{self.data_folder}/*.md",
            f"{self.data_folder}/*.txt", 
            f"{self.data_folder}/*.csv"
        ]
        
        current_max_time = 0
        for pattern in patterns:
            for file_path in glob.glob(pattern):
                file_time = os.path.getmtime(file_path)
                current_max_time = max(current_max_time, file_time)
        
        return current_max_time > self.files_timestamp
    
    def process_files(self) -> Dict[str, Any]:
        processed_files = []
        errors = []
        
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder, exist_ok=True)
            return {
                "message": "Created data/documents/ folder.",
                "processed_files": [],
                "total_files": 0,
                "knowledge_base_ready": False,
                "errors": []
            }
        
        patterns = [
            f"{self.data_folder}/*.md",
            f"{self.data_folder}/*.txt", 
            f"{self.data_folder}/*.csv"
        ]
        
        files = []
        for pattern in patterns:
            files.extend(glob.glob(pattern))
        
        if not files:
            return {
                "message": "No supported files found in data/documents/ folder.",
                "processed_files": [],
                "total_files": 0,
                "knowledge_base_ready": False,
                "errors": []
            }
        
        self.knowledge_base = {}
        
        for file_path in files:
            try:
                filename = os.path.basename(file_path)
                content = self._read_file(file_path)
                
                if content:
                    self.knowledge_base[filename] = content
                    processed_files.append(filename)
                
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")
        
        import time
        self.files_timestamp = time.time()
        
        return {
            "message": f"Processed {len(processed_files)} file(s) successfully.",
            "processed_files": processed_files,
            "total_files": len(processed_files),
            "errors": errors,
            "knowledge_base_ready": len(processed_files) > 0
        }
    
    def _read_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext in ['.md', '.txt']:
                    return file.read()
                
                elif ext == '.csv':
                    content = []
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        if i == 0:
                            content.append(f"Cabeçalho: {line.strip()}")
                        else:
                            content.append(line.strip())
                    return "\n".join(content)
                
        except Exception as e:
            raise Exception(f"Error reading file: {e}")
    
    def chat(self, message: str) -> Dict[str, Any]:
        # Auto-load or reload files if needed
        if not self.knowledge_base or self._has_new_files():
            files_result = self.process_files()
            if not files_result.get("processed_files"):
                return {
                    "response": "Nenhum arquivo encontrado em data/documents/",
                    "sources": []
                }
        
        relevant_docs = []
        message_lower = message.lower()
        
        for filename, content in self.knowledge_base.items():
            content_lower = content.lower()
            if any(word in content_lower for word in message_lower.split() if len(word) > 3):
                relevant_docs.append((filename, content))
        
        if not relevant_docs:
            relevant_docs = list(self.knowledge_base.items())
        
        context = ""
        used_sources = []
        max_context_length = 3000
        
        for filename, content in relevant_docs[:3]:  # Max 3 documents
            if len(context) + len(content) < max_context_length:
                context += f"\n--- {filename} ---\n{content}\n"
                used_sources.append(filename)
            else:
                remaining_space = max_context_length - len(context)
                if remaining_space > 100:
                    context += f"\n--- {filename} (parcial) ---\n{content[:remaining_space]}\n"
                    used_sources.append(f"{filename} (parcial)")
                break
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": self.system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Contexto:\n{context}\n\nPergunta: {message}"
                    }
                ],
                max_tokens=500,
                temperature=self.temperature
            )
            
            return {
                "response": response.choices[0].message.content,
                "sources": used_sources
            }
            
        except Exception as e:
            return {
                "response": f"Erro ao gerar resposta: {str(e)}.",
                "sources": used_sources
            }
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "knowledge_base_loaded": len(self.knowledge_base) > 0,
            "files_count": len(self.knowledge_base),
            "loaded_files": list(self.knowledge_base.keys()),
            "data_folder": self.data_folder,
            "supported_formats": [".md", ".txt", ".csv"]
        }
