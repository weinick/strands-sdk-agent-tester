"""
File Manager Agent - Specialized agent for file operations and management
Demonstrates advanced file handling capabilities with Strands SDK
"""

import os
import sys
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging
import mimetypes
import stat

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
except ImportError:
    print("Warning: boto3 not installed. Install with: pip install boto3")
    boto3 = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileOperationsTool:
    """Advanced file operations tool"""
    
    @staticmethod
    def list_directory(path: str = ".", detailed: bool = False, recursive: bool = False) -> str:
        """List directory contents with optional details"""
        try:
            target_path = Path(path).resolve()
            
            if not target_path.exists():
                return f"❌ Path does not exist: {path}"
            
            if not target_path.is_dir():
                return f"❌ Not a directory: {path}"
            
            result = f"📁 **Directory Listing: {target_path}**\n\n"
            
            if recursive:
                items = list(target_path.rglob("*"))
                result += f"**Recursive listing ({len(items)} items):**\n"
            else:
                items = list(target_path.iterdir())
                result += f"**Contents ({len(items)} items):**\n"
            
            # Separate directories and files
            directories = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            # List directories first
            if directories:
                result += "\n**📁 Directories:**\n"
                for directory in sorted(directories):
                    if detailed:
                        stat_info = directory.stat()
                        mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        result += f"  📁 {directory.name}/ (modified: {mod_time})\n"
                    else:
                        result += f"  📁 {directory.name}/\n"
            
            # List files
            if files:
                result += "\n**📄 Files:**\n"
                total_size = 0
                for file in sorted(files):
                    stat_info = file.stat()
                    size = stat_info.st_size
                    total_size += size
                    
                    if detailed:
                        mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                        size_str = FileOperationsTool._format_size(size)
                        mime_type = mimetypes.guess_type(file)[0] or "unknown"
                        result += f"  📄 {file.name} ({size_str}, {mime_type}, modified: {mod_time})\n"
                    else:
                        size_str = FileOperationsTool._format_size(size)
                        result += f"  📄 {file.name} ({size_str})\n"
                
                if detailed:
                    result += f"\n**Summary:**\n"
                    result += f"• Total files: {len(files)}\n"
                    result += f"• Total directories: {len(directories)}\n"
                    result += f"• Total size: {FileOperationsTool._format_size(total_size)}\n"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied accessing: {path}"
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"
    
    @staticmethod
    def read_file(filepath: str, max_lines: int = 50, encoding: str = "utf-8") -> str:
        """Read file contents with encoding detection"""
        try:
            file_path = Path(filepath).resolve()
            
            if not file_path.exists():
                return f"❌ File does not exist: {filepath}"
            
            if not file_path.is_file():
                return f"❌ Not a file: {filepath}"
            
            # Get file info
            stat_info = file_path.stat()
            size = stat_info.st_size
            mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            mime_type = mimetypes.guess_type(file_path)[0] or "unknown"
            
            # Check if file is too large
            if size > 1024 * 1024:  # 1MB
                return f"❌ File too large to display: {FileOperationsTool._format_size(size)} (limit: 1MB)"
            
            # Try to read the file
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                # Try with different encodings
                for enc in ['latin-1', 'cp1252', 'utf-16']:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            lines = f.readlines()
                        encoding = enc
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    return f"❌ Cannot decode file with common encodings: {filepath}"
            
            result = f"📄 **File: {file_path.name}**\n\n"
            result += f"**File Information:**\n"
            result += f"• Path: {file_path}\n"
            result += f"• Size: {FileOperationsTool._format_size(size)}\n"
            result += f"• Type: {mime_type}\n"
            result += f"• Encoding: {encoding}\n"
            result += f"• Modified: {mod_time}\n"
            result += f"• Lines: {len(lines)}\n\n"
            
            if len(lines) <= max_lines:
                content = ''.join(lines)
                result += f"**Content:**\n```\n{content}\n```"
            else:
                content = ''.join(lines[:max_lines])
                result += f"**Content (first {max_lines} lines of {len(lines)}):**\n```\n{content}\n```"
                result += f"\n*Use 'read file {filepath} all' to see the complete file*"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied reading: {filepath}"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    @staticmethod
    def file_info(filepath: str) -> str:
        """Get detailed file information"""
        try:
            file_path = Path(filepath).resolve()
            
            if not file_path.exists():
                return f"❌ Path does not exist: {filepath}"
            
            stat_info = file_path.stat()
            
            result = f"ℹ️ **File Information: {file_path.name}**\n\n"
            result += f"**Basic Info:**\n"
            result += f"• Full Path: {file_path}\n"
            result += f"• Type: {'Directory' if file_path.is_dir() else 'File'}\n"
            result += f"• Size: {FileOperationsTool._format_size(stat_info.st_size)}\n"
            
            if file_path.is_file():
                mime_type = mimetypes.guess_type(file_path)[0] or "unknown"
                result += f"• MIME Type: {mime_type}\n"
            
            result += f"\n**Timestamps:**\n"
            result += f"• Created: {datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"• Modified: {datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"• Accessed: {datetime.fromtimestamp(stat_info.st_atime).strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            result += f"\n**Permissions:**\n"
            mode = stat_info.st_mode
            result += f"• Mode: {stat.filemode(mode)}\n"
            result += f"• Readable: {'Yes' if os.access(file_path, os.R_OK) else 'No'}\n"
            result += f"• Writable: {'Yes' if os.access(file_path, os.W_OK) else 'No'}\n"
            result += f"• Executable: {'Yes' if os.access(file_path, os.X_OK) else 'No'}\n"
            
            if file_path.is_file():
                # Calculate file hash for integrity
                with open(file_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                result += f"\n**Integrity:**\n"
                result += f"• MD5 Hash: {file_hash}\n"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied accessing: {filepath}"
        except Exception as e:
            return f"❌ Error getting file info: {str(e)}"
    
    @staticmethod
    def search_files(directory: str = ".", pattern: str = "*", content_search: str = None) -> str:
        """Search for files by name pattern or content"""
        try:
            search_path = Path(directory).resolve()
            
            if not search_path.exists():
                return f"❌ Directory does not exist: {directory}"
            
            if not search_path.is_dir():
                return f"❌ Not a directory: {directory}"
            
            result = f"🔍 **File Search Results**\n\n"
            result += f"**Search Parameters:**\n"
            result += f"• Directory: {search_path}\n"
            result += f"• Pattern: {pattern}\n"
            if content_search:
                result += f"• Content Search: '{content_search}'\n"
            result += f"• Search Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            # Find files matching pattern
            matching_files = list(search_path.rglob(pattern))
            
            if content_search:
                # Filter by content
                content_matches = []
                for file_path in matching_files:
                    if file_path.is_file():
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                if content_search.lower() in content.lower():
                                    content_matches.append(file_path)
                        except:
                            continue
                matching_files = content_matches
            
            if not matching_files:
                result += "**No files found matching the criteria.**"
                return result
            
            result += f"**Found {len(matching_files)} matching files:**\n\n"
            
            for file_path in sorted(matching_files):
                if file_path.is_file():
                    stat_info = file_path.stat()
                    size = FileOperationsTool._format_size(stat_info.st_size)
                    mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M')
                    relative_path = file_path.relative_to(search_path)
                    result += f"📄 {relative_path} ({size}, {mod_time})\n"
                elif file_path.is_dir():
                    relative_path = file_path.relative_to(search_path)
                    result += f"📁 {relative_path}/\n"
            
            return result
            
        except PermissionError:
            return f"❌ Permission denied searching: {directory}"
        except Exception as e:
            return f"❌ Error searching files: {str(e)}"
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

class FileManagerAgent:
    """
    Advanced agent specialized in file operations and management
    """
    
    def __init__(self, model_config: Optional[Dict[str, Any]] = None):
        """Initialize the file manager agent"""
        self.model_config = model_config or {
            "provider": "AWS Bedrock",
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "temperature": 0.5,
            "max_tokens": 1200
        }
        
        self.conversation_history = []
        self.operation_history = []
        self.bedrock_client = None
        self.current_directory = Path.cwd()
        
        # Initialize file operations tool
        self.file_ops = FileOperationsTool()
        
        # Initialize Bedrock client if using AWS
        if self.model_config.get("provider") == "AWS Bedrock":
            self._init_bedrock_client()
    
    def _init_bedrock_client(self):
        """Initialize AWS Bedrock client"""
        try:
            if boto3:
                self.bedrock_client = boto3.client(
                    'bedrock-runtime',
                    region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
                )
                logger.info("✅ AWS Bedrock client initialized successfully")
            else:
                logger.warning("⚠️ boto3 not available, using mock responses")
        except NoCredentialsError:
            logger.error("❌ AWS credentials not found. Please configure AWS CLI or set environment variables")
        except Exception as e:
            logger.error(f"❌ Error initializing Bedrock client: {str(e)}")
    
    def chat(self, user_input: str) -> str:
        """Process file management requests"""
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            
            # Check for file operation requests
            file_response = self._handle_file_operations(user_input)
            
            if file_response:
                response = file_response
            else:
                # Generate conversational response
                if self.bedrock_client and self.model_config.get("provider") == "AWS Bedrock":
                    response = self._call_bedrock(user_input)
                else:
                    response = self._generate_conversational_response(user_input)
            
            # Add response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Error processing file operation: {str(e)}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
    
    def _handle_file_operations(self, user_input: str) -> Optional[str]:
        """Handle file operation requests"""
        user_lower = user_input.lower()
        
        # List directory operations
        if any(phrase in user_lower for phrase in ['list files', 'show files', 'ls', 'dir']):
            directory = self._extract_path(user_input) or "."
            detailed = 'detailed' in user_lower or '-l' in user_input
            recursive = 'recursive' in user_lower or '-r' in user_input
            
            result = self.file_ops.list_directory(directory, detailed, recursive)
            self._log_operation("list_directory", {"path": directory, "detailed": detailed, "recursive": recursive})
            return result
        
        # Read file operations
        elif any(phrase in user_lower for phrase in ['read file', 'show file', 'cat', 'open file']):
            filepath = self._extract_path(user_input)
            if not filepath:
                return "📄 Please specify which file you'd like me to read."
            
            max_lines = 50
            if 'all' in user_lower:
                max_lines = float('inf')
            
            result = self.file_ops.read_file(filepath, max_lines)
            self._log_operation("read_file", {"path": filepath})
            return result
        
        # File info operations
        elif any(phrase in user_lower for phrase in ['file info', 'info about', 'details of']):
            filepath = self._extract_path(user_input)
            if not filepath:
                return "ℹ️ Please specify which file or directory you'd like info about."
            
            result = self.file_ops.file_info(filepath)
            self._log_operation("file_info", {"path": filepath})
            return result
        
        # Search operations
        elif any(phrase in user_lower for phrase in ['search for', 'find files', 'search files']):
            directory = "."
            pattern = "*"
            content_search = None
            
            # Extract search parameters (simplified)
            if 'in' in user_lower:
                parts = user_input.split('in')
                if len(parts) > 1:
                    directory = parts[-1].strip()
            
            if '"' in user_input:
                import re
                quotes = re.findall(r'"([^"]*)"', user_input)
                if quotes:
                    if 'content' in user_lower:
                        content_search = quotes[0]
                    else:
                        pattern = quotes[0]
            
            result = self.file_ops.search_files(directory, pattern, content_search)
            self._log_operation("search_files", {"directory": directory, "pattern": pattern, "content": content_search})
            return result
        
        # Current directory operations
        elif any(phrase in user_lower for phrase in ['current directory', 'where am i', 'pwd']):
            return f"📍 **Current Directory:** {self.current_directory}"
        
        return None
    
    def _extract_path(self, user_input: str) -> Optional[str]:
        """Extract file/directory path from user input"""
        # Simple path extraction - look for quoted paths or common file extensions
        import re
        
        # Check for quoted paths
        quoted_match = re.search(r'"([^"]*)"', user_input)
        if quoted_match:
            return quoted_match.group(1)
        
        # Check for file extensions
        file_match = re.search(r'\b[\w\-_./]+\.\w+\b', user_input)
        if file_match:
            return file_match.group(0)
        
        # Check for directory-like paths
        path_match = re.search(r'\b[\w\-_./]+/[\w\-_./]*\b', user_input)
        if path_match:
            return path_match.group(0)
        
        # Look for single word that might be a filename
        words = user_input.split()
        for word in words:
            if '.' in word and not word.startswith('.'):
                return word
        
        return None
    
    def _log_operation(self, operation: str, params: Dict[str, Any]):
        """Log file operations"""
        self.operation_history.append({
            "operation": operation,
            "params": params,
            "timestamp": datetime.now(),
            "directory": str(self.current_directory)
        })
    
    def _call_bedrock(self, user_input: str) -> str:
        """Call AWS Bedrock for file management responses"""
        try:
            system_message = """You are a specialized file management agent with capabilities for:
- Directory listing and navigation
- File reading and content analysis
- File search and filtering
- File information and metadata extraction
- File system operations and management

When users need file operations, I use specialized tools to provide comprehensive file management assistance.
For general conversation, I maintain a file management focus."""
            
            messages = [{"role": "user", "content": f"{system_message}\n\nUser: {user_input}"}]
            
            if "claude" in self.model_config["model"].lower():
                body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.model_config.get("max_tokens", 1200),
                    "temperature": self.model_config.get("temperature", 0.5),
                    "messages": messages
                }
            else:
                body = {
                    "inputText": user_input,
                    "textGenerationConfig": {
                        "maxTokenCount": self.model_config.get("max_tokens", 1200),
                        "temperature": self.model_config.get("temperature", 0.5)
                    }
                }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_config["model"],
                body=json.dumps(body),
                contentType="application/json"
            )
            
            response_body = json.loads(response['body'].read())
            
            if "claude" in self.model_config["model"].lower():
                return response_body['content'][0]['text']
            else:
                return response_body.get('results', [{}])[0].get('outputText', 'No response generated')
                
        except Exception as e:
            return f"❌ Bedrock API error: {str(e)}"
    
    def _generate_conversational_response(self, user_input: str) -> str:
        """Generate file management focused responses"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return f"""Hello! I'm a File Manager Agent specialized in file operations and management.

📁 **Current Directory:** {self.current_directory}

🛠️ **File Operations I Can Perform:**
• **List Files**: "list files", "show files in [directory]"
• **Read Files**: "read file [filename]", "show file content"
• **File Info**: "file info [filename]", "details of [file]"
• **Search Files**: "search for [pattern]", "find files containing [text]"
• **Navigation**: "current directory", "where am i"

**Example Commands:**
• "list files in Documents"
• "read file README.md"
• "file info package.json"
• "search for *.py files"
• "find files containing 'TODO'"

How can I help you manage your files today?"""
        
        elif any(word in user_lower for word in ['what can you do', 'capabilities', 'help']):
            return f"""I'm a specialized File Manager Agent with comprehensive file handling capabilities:

📁 **Core File Operations:**

**Directory Management:**
• List directory contents (basic or detailed)
• Recursive directory traversal
• Directory size and structure analysis
• Permission and access checking

**File Operations:**
• Read file contents with encoding detection
• Display file information and metadata
• File size, type, and timestamp analysis
• Hash generation for integrity checking

**Search & Discovery:**
• Pattern-based file searching
• Content-based file filtering
• Recursive search capabilities
• Advanced search with multiple criteria

**File Analysis:**
• MIME type detection
• File permission analysis
• Modification and access time tracking
• File integrity verification

🔧 **Advanced Features:**
• Safe file handling with error recovery
• Multiple encoding support
• Large file handling with size limits
• Cross-platform path handling

**Current Session Info:**
• Working Directory: {self.current_directory}
• Operations Performed: {len(self.operation_history)}
• File System Access: Full read access

**Safety Features:**
• Read-only operations (no file modification)
• Permission checking before operations
• Error handling and graceful failures
• Path validation and security checks

Ready to help you navigate and manage your file system efficiently!"""
        
        elif any(word in user_lower for word in ['goodbye', 'bye', 'thanks']):
            return f"""Thank you for using the File Manager Agent!

**Session Summary:**
• Operations Performed: {len(self.operation_history)}
• Working Directory: {self.current_directory}
• File Management Tasks: Completed successfully

**Operations Available:**
📁 Directory Listing | 📄 File Reading | 🔍 File Search | ℹ️ File Information

Feel free to return anytime for:
• File system navigation
• Content analysis and reading
• File search and discovery
• File information and metadata

Keep your files organized! 📂✨"""
        
        else:
            return f"""I received your message: "{user_input}"

As a File Manager Agent, I can help you with various file operations:

📁 **Directory Operations:**
• "list files" - Show current directory contents
• "list files in [path]" - Show specific directory
• "list files detailed" - Show with full details

📄 **File Operations:**
• "read file [filename]" - Display file contents
• "file info [filename]" - Show file details
• "show file [filename]" - Read file content

🔍 **Search Operations:**
• "search for *.txt" - Find files by pattern
• "find files containing [text]" - Content search
• "search files in [directory]" - Directory-specific search

**Current Context:**
• Working Directory: {self.current_directory}
• Operations History: {len(self.operation_history)} operations
• Provider: {self.model_config.get('provider', 'Mock')}
• Model: {self.model_config.get('model', 'File Manager Demo')}

What file operation would you like me to perform? I'm ready to help you navigate and manage your file system!"""
    
    def get_operation_history(self) -> List[Dict]:
        """Get operation history"""
        return self.operation_history.copy()
    
    def get_available_tools(self) -> List[str]:
        """Get list of available file tools"""
        return ["Directory Listing", "File Reading", "File Information", "File Search"]
    
    def get_conversation_history(self) -> list:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear conversation and operation history"""
        self.conversation_history = []
        self.operation_history = []
        logger.info("All history cleared")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_type": "File Manager Agent",
            "model_config": self.model_config,
            "available_tools": self.get_available_tools(),
            "conversation_length": len(self.conversation_history),
            "operations_performed": len(self.operation_history),
            "current_directory": str(self.current_directory),
            "bedrock_available": self.bedrock_client is not None,
            "status": "Ready for File Operations"
        }

def create_file_manager_agent(model_config: Optional[Dict[str, Any]] = None) -> FileManagerAgent:
    """Factory function to create a File Manager Agent"""
    return FileManagerAgent(model_config)

def main():
    """Main function for testing the agent directly"""
    print("📁 File Manager Agent - Strands SDK Demo")
    print("=" * 60)
    
    # Create agent
    agent = create_file_manager_agent()
    
    print("File Manager Agent initialized with tools:", agent.get_available_tools())
    print("Status:", agent.get_status())
    print("-" * 60)
    print("Try file commands like:")
    print('• "list files"')
    print('• "read file README.md"')
    print('• "file info package.json"')
    print('• "search for *.py"')
    print('• "current directory"')
    print("• Type 'quit' to exit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nAgent: Thank you for using the File Manager Agent!")
                break
            
            if user_input:
                response = agent.chat(user_input)
                print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the File Manager Agent!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
