#!/usr/bin/env python3
"""
Backup script for XLZR-v3 Discord Bot data
Creates timestamped backups of all bot data files.
"""

import os
import json
import shutil
from datetime import datetime

def create_backup():
    """Create a timestamped backup of all data files"""
    if not os.path.exists('data'):
        print("❌ No data directory found")
        return
    
    # Create backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/backup_{timestamp}"
    
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    os.makedirs(backup_dir)
    
    # Copy all data files
    data_files = [
        'guild_configs.json',
        'user_levels.json', 
        'user_warnings.json',
        'verification_data.json',
        'keyword_config.json'
    ]
    
    backed_up_files = 0
    for filename in data_files:
        source = os.path.join('data', filename)
        if os.path.exists(source):
            destination = os.path.join(backup_dir, filename)
            shutil.copy2(source, destination)
            backed_up_files += 1
            print(f"✅ Backed up: {filename}")
    
    if backed_up_files > 0:
        print(f"\n🎉 Backup created successfully!")
        print(f"📁 Location: {backup_dir}")
        print(f"📊 Files backed up: {backed_up_files}")
    else:
        print("❌ No data files found to backup")
        os.rmdir(backup_dir)

def list_backups():
    """List all available backups"""
    if not os.path.exists('backups'):
        print("❌ No backups directory found")
        return
    
    backups = [d for d in os.listdir('backups') if d.startswith('backup_')]
    
    if not backups:
        print("❌ No backups found")
        return
    
    print("📋 Available backups:")
    for backup in sorted(backups, reverse=True):
        timestamp = backup.replace('backup_', '')
        formatted_time = datetime.strptime(timestamp, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        print(f"  • {backup} ({formatted_time})")

def restore_backup(backup_name):
    """Restore from a specific backup"""
    backup_dir = os.path.join('backups', backup_name)
    
    if not os.path.exists(backup_dir):
        print(f"❌ Backup not found: {backup_name}")
        return
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Copy files from backup
    restored_files = 0
    for filename in os.listdir(backup_dir):
        if filename.endswith('.json'):
            source = os.path.join(backup_dir, filename)
            destination = os.path.join('data', filename)
            shutil.copy2(source, destination)
            restored_files += 1
            print(f"✅ Restored: {filename}")
    
    print(f"\n🎉 Restore completed!")
    print(f"📊 Files restored: {restored_files}")

def main():
    """Main backup function"""
    import sys
    
    if len(sys.argv) < 2:
        print("🗄️  XLZR-v3 Backup Utility")
        print("=" * 30)
        print("Usage:")
        print("  python scripts/backup_data.py create    - Create new backup")
        print("  python scripts/backup_data.py list      - List all backups")
        print("  python scripts/backup_data.py restore <backup_name> - Restore from backup")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        create_backup()
    elif command == 'list':
        list_backups()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Please specify backup name")
            list_backups()
        else:
            restore_backup(sys.argv[2])
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main()
