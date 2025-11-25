import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
from filesystem.file_system import FileSystem
from filesystem.node import File, Directory
from filesystem.permissions import Permissions


class FileSystemGUI:
    """Graphical user interface for the filesystem module"""
    
    def __init__(self, filesystem: FileSystem):
        self.fs = filesystem
        self.root = tk.Tk()
        self.root.title("OS Simulator - File System")
        self.root.geometry("1200x700")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.setup_ui()
        self.refresh_all()
    
    def setup_ui(self):
        """Initialize all UI components"""
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create paned window for resizable panels
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel: Directory tree
        tree_frame = ttk.LabelFrame(paned, text="Directory Tree", padding=5)
        paned.add(tree_frame, weight=1)
        self.create_tree_view(tree_frame)
        
        # Middle panel: File list
        list_frame = ttk.LabelFrame(paned, text="Files and Directories", padding=5)
        paned.add(list_frame, weight=2)
        self.create_file_list(list_frame)
        
        # Right panel: Properties
        props_frame = ttk.LabelFrame(paned, text="Properties", padding=5)
        paned.add(props_frame, weight=1)
        self.create_properties_panel(props_frame)
        
        # Status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.create_file, accelerator="Ctrl+N")
        file_menu.add_command(label="New Directory", command=self.create_directory, accelerator="Ctrl+Shift+N")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Rename", command=self.rename_item, accelerator="F2")
        edit_menu.add_command(label="Delete", command=self.delete_item, accelerator="Delete")
        edit_menu.add_separator()
        edit_menu.add_command(label="Permissions", command=self.change_permissions, accelerator="Ctrl+P")
        edit_menu.add_command(label="Change Owner", command=self.change_owner, accelerator="Ctrl+O")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_all, accelerator="F5")
        
        # User menu
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="User", menu=user_menu)
        user_menu.add_command(label="Switch User", command=self.switch_user)
        user_menu.add_command(label="Add User (root only)", command=self.add_user)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Keyboard bindings
        self.root.bind("<Control-n>", lambda e: self.create_file())
        self.root.bind("<Control-N>", lambda e: self.create_directory())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
        self.root.bind("<F2>", lambda e: self.rename_item())
        self.root.bind("<Delete>", lambda e: self.delete_item())
        self.root.bind("<Control-p>", lambda e: self.change_permissions())
        self.root.bind("<Control-o>", lambda e: self.change_owner())
        self.root.bind("<F5>", lambda e: self.refresh_all())
    
    def create_toolbar(self):
        """Create toolbar with common operations"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        ttk.Button(toolbar, text="📄 New File", command=self.create_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📁 New Folder", command=self.create_directory).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="✏️ Rename", command=self.rename_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑️ Delete", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="🔒 Permissions", command=self.change_permissions).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="👤 Owner", command=self.change_owner).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="🔄 Refresh", command=self.refresh_all).pack(side=tk.LEFT, padx=2)
    
    def create_tree_view(self, parent):
        """Create directory tree view"""
        # Scrollbar
        scrollbar = ttk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Tree view
        self.tree = ttk.Treeview(parent, yscrollcommand=scrollbar.set, selectmode='browse')
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree['columns'] = ()
        self.tree.heading('#0', text='Directory Structure')
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Button-3>', self.show_tree_context_menu)
        
    def create_file_list(self, parent):
        """Create file list view"""
        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical")
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        hsb = ttk.Scrollbar(parent, orient="horizontal")
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # File list
        self.file_list = ttk.Treeview(
            parent,
            columns=('type', 'permissions', 'owner', 'size', 'modified'),
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            selectmode='browse'
        )
        self.file_list.pack(fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.file_list.yview)
        hsb.config(command=self.file_list.xview)
        
        # Configure columns
        self.file_list.heading('#0', text='Name')
        self.file_list.heading('type', text='Type')
        self.file_list.heading('permissions', text='Permissions')
        self.file_list.heading('owner', text='Owner')
        self.file_list.heading('size', text='Size')
        self.file_list.heading('modified', text='Modified')
        
        self.file_list.column('#0', width=200)
        self.file_list.column('type', width=80)
        self.file_list.column('permissions', width=100)
        self.file_list.column('owner', width=80)
        self.file_list.column('size', width=80)
        self.file_list.column('modified', width=150)
        
        # Bind events
        self.file_list.bind('<<TreeviewSelect>>', self.on_file_select)
        self.file_list.bind('<Double-1>', self.on_file_double_click)
        self.file_list.bind('<Button-3>', self.show_file_context_menu)
    
    def create_properties_panel(self, parent):
        """Create properties panel"""
        self.props_text = tk.Text(parent, height=10, width=30, wrap=tk.WORD, state='disabled')
        self.props_text.pack(fill=tk.BOTH, expand=True)
        
        # Permission editor frame
        perm_frame = ttk.LabelFrame(parent, text="Edit Permissions", padding=5)
        perm_frame.pack(fill=tk.X, pady=5)
        
        # Permission checkboxes
        self.perm_vars = {}
        for category, label in [('owner', 'Owner'), ('group', 'Group'), ('others', 'Others')]:
            cat_frame = ttk.LabelFrame(perm_frame, text=label, padding=3)
            cat_frame.pack(fill=tk.X, pady=2)
            
            self.perm_vars[category] = {}
            for perm in ['read', 'write', 'execute']:
                var = tk.BooleanVar()
                ttk.Checkbutton(cat_frame, text=perm.capitalize(), variable=var).pack(side=tk.LEFT, padx=5)
                self.perm_vars[category][perm] = var
        
        # Apply button
        ttk.Button(perm_frame, text="Apply Permissions", command=self.apply_permissions).pack(pady=5)
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_user = ttk.Label(status_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_user.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        
        self.status_path = ttk.Label(status_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
    
    def refresh_all(self):
        """Refresh all views"""
        self.refresh_tree()
        self.refresh_file_list()
        self.update_status_bar()
    
    def refresh_tree(self):
        """Refresh directory tree"""
        self.tree.delete(*self.tree.get_children())
        self._populate_tree('', self.fs.root, '/')
        
    def _populate_tree(self, parent_id, directory, path):
        """Recursively populate tree view"""
        node_id = self.tree.insert(parent_id, 'end', text=path if path == '/' else directory.name, 
                                    values=(path,), tags=('directory',))
        
        # Add children
        for child in directory.children.values():
            if isinstance(child, Directory):
                child_path = f"{path}{child.name}/" if path == '/' else f"{path}/{child.name}"
                self._populate_tree(node_id, child, child_path)
    
    def refresh_file_list(self):
        """Refresh file list for current directory"""
        self.file_list.delete(*self.file_list.get_children())
        
        current_dir = self.fs.current_dir
        
        # Add parent directory if not root
        if current_dir != self.fs.root:
            self.file_list.insert('', 'end', text='..', values=('DIR', '', '', '', ''), tags=('parent',))
        
        # Add children
        for name, node in sorted(current_dir.children.items()):
            node_type = 'DIR' if isinstance(node, Directory) else 'FILE'
            perms = node.permissions.to_string()
            owner = node.owner.username
            size = str(len(node._content)) if isinstance(node, File) else ''
            modified = node.modified_at.strftime('%Y-%m-%d %H:%M:%S')
            
            icon = '📁' if isinstance(node, Directory) else '📄'
            display_name = f"{icon} {name}"
            
            self.file_list.insert('', 'end', text=display_name, 
                                 values=(node_type, perms, owner, size, modified),
                                 tags=(node_type.lower(),))
    
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            path = item['values'][0] if item['values'] else '/'
            
            try:
                self.fs.cd(path)
                self.refresh_file_list()
                self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def on_file_select(self, event):
        """Handle file list selection"""
        selection = self.file_list.selection()
        if selection:
            item = self.file_list.item(selection[0])
            name = item['text'].replace('📁 ', '').replace('📄 ', '')
            
            if name == '..':
                return
            
            try:
                node = self.fs.current_dir.children.get(name)
                if node:
                    self.update_properties(node)
            except Exception as e:
                pass
    
    def on_file_double_click(self, event):
        """Handle double-click on file list"""
        selection = self.file_list.selection()
        if not selection:
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            # Go to parent directory
            try:
                self.fs.cd('..')
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            node = self.fs.current_dir.children.get(name)
            if isinstance(node, Directory):
                # Navigate to directory
                try:
                    self.fs.cd(name)
                    self.refresh_all()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            elif isinstance(node, File):
                # View file content
                self.view_file_content()
    
    def update_properties(self, node):
        """Update properties panel"""
        self.props_text.config(state='normal')
        self.props_text.delete(1.0, tk.END)
        
        props = f"Name: {node.name}\n"
        props += f"Type: {'Directory' if isinstance(node, Directory) else 'File'}\n"
        props += f"Owner: {node.owner.username}\n"
        props += f"Permissions: {node.permissions.to_string()}\n"
        props += f"Created: {node.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        props += f"Modified: {node.modified_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        if isinstance(node, File):
            props += f"Size: {len(node._content)} bytes\n"
        
        self.props_text.insert(1.0, props)
        self.props_text.config(state='disabled')
        
        # Update permission checkboxes
        perms = node.permissions
        self.perm_vars['owner']['read'].set(perms.owner_read)
        self.perm_vars['owner']['write'].set(perms.owner_write)
        self.perm_vars['owner']['execute'].set(perms.owner_execute)
        self.perm_vars['group']['read'].set(perms.group_read)
        self.perm_vars['group']['write'].set(perms.group_write)
        self.perm_vars['group']['execute'].set(perms.group_execute)
        self.perm_vars['others']['read'].set(perms.others_read)
        self.perm_vars['others']['write'].set(perms.others_write)
        self.perm_vars['others']['execute'].set(perms.others_execute)
    
    def update_status_bar(self):
        """Update status bar"""
        self.status_user.config(text=f" User: {self.fs.current_user.username} (UID: {self.fs.current_user.uid})")
        self.status_path.config(text=f" Path: {self.fs.pwd()}")
    
    def create_file(self):
        """Create a new file"""
        filename = simpledialog.askstring("New File", "Enter file name:")
        if filename:
            try:
                self.fs.touch(filename)
                self.refresh_all()
                messagebox.showinfo("Success", f"File '{filename}' created successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def create_directory(self):
        """Create a new directory"""
        dirname = simpledialog.askstring("New Directory", "Enter directory name:")
        if dirname:
            try:
                self.fs.mkdir(dirname)
                self.refresh_all()
                messagebox.showinfo("Success", f"Directory '{dirname}' created successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def delete_item(self):
        """Delete selected item"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            return
        
        node = self.fs.current_dir.children.get(name)
        if not node:
            return
        
        is_dir = isinstance(node, Directory)
        msg = f"Are you sure you want to delete {'directory' if is_dir else 'file'} '{name}'?"
        
        if is_dir and node.children:
            msg += "\n\nThis directory is not empty. All contents will be deleted."
        
        if messagebox.askyesno("Confirm Delete", msg):
            try:
                self.fs.rm(name, recursive=True)
                self.refresh_all()
                messagebox.showinfo("Success", f"{'Directory' if is_dir else 'File'} '{name}' deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def rename_item(self):
        """Rename selected item"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to rename")
            return
        
        item = self.file_list.item(selection[0])
        old_name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if old_name == '..':
            return
        
        new_name = simpledialog.askstring("Rename", f"Enter new name for '{old_name}':", 
                                         initialvalue=old_name)
        if new_name and new_name != old_name:
            try:
                node = self.fs.current_dir.children.get(old_name)
                if node:
                    # Simple rename by changing the name attribute
                    del self.fs.current_dir.children[old_name]
                    node.name = new_name
                    self.fs.current_dir.children[new_name] = node
                    self.refresh_all()
                    messagebox.showinfo("Success", f"Renamed '{old_name}' to '{new_name}'")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def change_permissions(self):
        """Open permission dialog"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            return
        
        # The apply_permissions method will handle the actual change
        messagebox.showinfo("Permissions", 
                          "Edit the permissions using the checkboxes in the Properties panel and click 'Apply Permissions'")
    
    def apply_permissions(self):
        """Apply permission changes"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            return
        
        try:
            # Build octal permission string
            perms = ''
            for category in ['owner', 'group', 'others']:
                val = 0
                if self.perm_vars[category]['read'].get():
                    val += 4
                if self.perm_vars[category]['write'].get():
                    val += 2
                if self.perm_vars[category]['execute'].get():
                    val += 1
                perms += str(val)
            
            self.fs.chmod(name, perms)
            self.refresh_all()
            
            # Re-select the item
            for child in self.file_list.get_children():
                if self.file_list.item(child)['text'].replace('📁 ', '').replace('📄 ', '') == name:
                    self.file_list.selection_set(child)
                    break
            
            messagebox.showinfo("Success", f"Permissions updated to {perms}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def change_owner(self):
        """Change file owner"""
        selection = self.file_list.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            return
        
        # Get list of users
        users = list(self.fs.users.keys())
        user_list = "\n".join(users)
        
        new_owner = simpledialog.askstring("Change Owner", 
                                          f"Available users:\n{user_list}\n\nEnter new owner:")
        if new_owner:
            try:
                self.fs.chown(name, new_owner)
                self.refresh_all()
                messagebox.showinfo("Success", f"Owner changed to '{new_owner}'")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def view_file_content(self):
        """View file content in a dialog"""
        selection = self.file_list.selection()
        if not selection:
            return
        
        item = self.file_list.item(selection[0])
        name = item['text'].replace('📁 ', '').replace('📄 ', '')
        
        if name == '..':
            return
        
        try:
            content = self.fs.cat(name)
            
            # Create dialog
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Edit File: {name}")
            dialog.geometry("600x400")
            
            # Instructions label
            ttk.Label(dialog, text="Edit the file content below and click Save:", 
                     font=('Arial', 10, 'bold')).pack(padx=5, pady=5, anchor=tk.W)
            
            # Text widget with scrollbar
            text_frame = ttk.Frame(dialog)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            scrollbar = ttk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text.pack(fill=tk.BOTH, expand=True)
            scrollbar.config(command=text.yview)
            
            text.insert(1.0, content)
            text.focus()
            
            # Button frame
            btn_frame = ttk.Frame(dialog)
            btn_frame.pack(fill=tk.X, padx=5, pady=5)
            
            def save_and_close():
                self.edit_file_content_dialog(name, text, dialog)
            
            ttk.Button(btn_frame, text="💾 Save", command=save_and_close, 
                      style='Accent.TButton').pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=2)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def edit_file_content_dialog(self, filename, text_widget, dialog=None):
        """Save edited file content"""
        content = text_widget.get(1.0, tk.END).rstrip('\n')
        
        try:
            self.fs.echo(filename, content, append=False)
            messagebox.showinfo("Success", f"File '{filename}' saved successfully")
            self.refresh_file_list()
            if dialog:
                dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def switch_user(self):
        """Switch to a different user"""
        users = list(self.fs.users.keys())
        user_list = "\n".join(users)
        
        username = simpledialog.askstring("Switch User", 
                                         f"Available users:\n{user_list}\n\nEnter username:")
        if username:
            try:
                self.fs.switch_user(username)
                self.refresh_all()
                messagebox.showinfo("Success", f"Switched to user '{username}'")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def add_user(self):
        """Add a new user (root only)"""
        if self.fs.current_user.uid != 0:
            messagebox.showerror("Error", "Only root can add users")
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add User")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        username_entry = ttk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="UID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        uid_entry = ttk.Entry(dialog)
        uid_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(dialog, text="Groups (comma-separated):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        groups_entry = ttk.Entry(dialog)
        groups_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def add():
            username = username_entry.get()
            uid_str = uid_entry.get()
            groups_str = groups_entry.get()
            
            if not username or not uid_str:
                messagebox.showerror("Error", "Username and UID are required")
                return
            
            try:
                uid = int(uid_str)
                groups = [g.strip() for g in groups_str.split(',')] if groups_str else ['users']
                self.fs.add_user(username, uid, groups)
                messagebox.showinfo("Success", f"User '{username}' added successfully")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "UID must be a number")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ttk.Button(dialog, text="Add", command=add).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=1, padx=5, pady=10)
    
    def show_tree_context_menu(self, event):
        """Show context menu for tree view"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="New Directory", command=self.create_directory)
        menu.add_command(label="Refresh", command=self.refresh_all)
        menu.post(event.x_root, event.y_root)
    
    def show_file_context_menu(self, event):
        """Show context menu for file list"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="New File", command=self.create_file)
        menu.add_command(label="New Directory", command=self.create_directory)
        menu.add_separator()
        menu.add_command(label="Rename", command=self.rename_item)
        menu.add_command(label="Delete", command=self.delete_item)
        menu.add_separator()
        menu.add_command(label="Permissions", command=self.change_permissions)
        menu.add_command(label="Change Owner", command=self.change_owner)
        menu.add_separator()
        menu.add_command(label="Refresh", command=self.refresh_all)
        menu.post(event.x_root, event.y_root)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """OS Simulator - File System GUI
        
Version: 1.0
A graphical interface for the virtual filesystem module.

Features:
• Unix-style permissions (rwx)
• User management
• Hierarchical directory structure
• File operations (create, delete, rename, etc.)

Author: Juan Camilo Castro Montoya
Course: Operating Systems"""
        
        messagebox.showinfo("About", about_text)
    
    def exit_app(self):
        """Exit the application"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()
    
    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
