import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os

class DumpFileFixer:
    
    def check_second_file(self, scan_file, object_name):
        # Searches for object_name in scan_file and returns the info after the next 'type :'
        checked_info = {}
        count = 0
        count1 = False

        found_object = False
        found_type = False
        found_type2 = False
        found_EventType = False
        found_time_delay = False

        first_Scan = False
        found_limit = False
        found_normal = False

        found_ACCExpression = False

        """Process the entire dump file"""
        try:
            with open(scan_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(scan_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
            object_name = "Object : " + object_name
            for line in lines:
                count += 1
                if not first_Scan and not found_object and object_name in line:
                    found_object = True

                if not found_type and found_object and "Type : " in line: 
                    found_type = True
                    
                if not found_EventType and found_type and "EventType : " in line:
                    # Get everything after 'EventType :'
                    EventType_info = line.split("EventType : ", 1)[1].strip()
                    found_EventType = True
                    count1 = True
                    
                if  not count1 and not found_type2 and found_EventType and "Type : " in line:
                    type_info = int(line.split("Type : ", 1)[1].strip())
                    found_type2 = True
                count1 = False       
                
                if not found_time_delay and found_type2 and "timeDelay : " in line:
                    time_delay_info = line.split("timeDelay : ", 1)[1].strip()
                    found_time_delay = True

                if found_object and found_type and found_type2 and found_EventType and found_time_delay:
                    first_Scan = True
                    # found_type2 = False
                    # found_EventType = False
                    # found_time_delay = False
                    # found_object = False
                    # found_type = False
                    #337
                if not found_limit and first_Scan and type_info == 337 and "Limit : " in line:
                    found_ACCExpression = True
                    Limit_info = line.split("Limit : ", 1)[1].strip()
                    found_limit = True
                if not found_normal and first_Scan and found_limit and type_info == 337 and "Normal : " in line:
                    Normal_info = line.split("Normal : ", 1)[1].strip()
                    found_normal = True                  
                    #340   
                if first_Scan and type_info == 340 and "ACCExpression : " in line:
                    found_normal = True
                    found_limit = True
                    ACCExpression_info = line.split("ACCExpression : ", 1)[1].strip()  
                    found_ACCExpression = True

                
                if first_Scan and found_normal and found_limit  and "MsgTextNormal : " in line:
                    MsgTextNormal_info = line.split("MsgTextNormal : ", 1)[1].strip()
                if first_Scan and found_normal and found_limit and "MsgTextOffNormal : " in line:
                    MsgTextOffNormal_info = line.split("MsgTextOffNormal : ", 1)[1].strip()
                if first_Scan and found_normal and found_limit and "MsgTextFault : " in line:
                    MsgTextFault_info = line.split("MsgTextFault : ", 1)[1].strip()
                if found_normal and found_limit and found_ACCExpression and "EndObject" in line:
                    # Reset flags for next object
                    first_Scan = False
                    found_object = False
                    found_type = False
                    found_type2 = False
                    found_EventType = False
                    found_time_delay = False
                    found_limit = False
                    found_normal = False

                    found_ACCExpression = False
                    
                    scanned_info = {
                        'EventType': EventType_info if 'EventType_info' in locals() else None,
                        'type': type_info if 'type_info' in locals() else None,
                        'timeDelay': time_delay_info if 'time_delay_info' in locals() else None,
                        'Limit': Limit_info if 'Limit_info' in locals() else None,
                        'Normal': Normal_info if 'Normal_info' in locals() else None,
                        'ACCExpression': ACCExpression_info if 'ACCExpression_info' in locals() else None,
                        'MsgTextNormal': MsgTextNormal_info if 'MsgTextNormal_info' in locals() else None,
                        'MsgTextOffNormal': MsgTextOffNormal_info if 'MsgTextOffNormal_info' in locals() else None,
                        'MsgTextFault': MsgTextFault_info if 'MsgTextFault_info' in locals() else None,
                    }
                    # Return the collected information as a dictionary
                    return scanned_info
                    # return {
                    #     'EventType': EventType_info,
                    #     'type': type_info,
                    #     'timeDelay': time_delay_info,
                    #     'Limit': Limit_info if 'Limit' in locals() else None,
                    #     'Normal': Normal_info if 'Normal' in locals() else None,
                    #     'ACCExpression': ACCExpression_info if 'ACCExpression' in locals() else None,
                    #     'MsgTextNormal': MsgTextNormal_info if 'MsgTextNormal' in locals() else None,
                    #     'MsgTextOffNormal': MsgTextOffNormal_info if 'MsgTextOffNormal' in locals() else None,
                    #     'MsgTextFault': MsgTextFault_info if 'MsgTextFault' in locals() else None,
                    # }
            scanned_info = {
                        'EventType': EventType_info if 'EventType_info' in locals() else None,
                        'type': type_info if 'type_info' in locals() else None,
                        'timeDelay': time_delay_info if 'time_delay_info' in locals() else None,
                        'Limit': Limit_info if 'Limit_info' in locals() else None,
                        'Normal': Normal_info if 'Normal_info' in locals() else None,
                        'ACCExpression': ACCExpression_info if 'ACCExpression_info' in locals() else None,
                        'MsgTextNormal': MsgTextNormal_info if 'MsgTextNormal_info' in locals() else None,
                        'MsgTextOffNormal': MsgTextOffNormal_info if 'MsgTextOffNormal_info' in locals() else None,
                        'MsgTextFault': MsgTextFault_info if 'MsgTextFault_info' in locals() else None,
                    }
            return scanned_info

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide main window
        self.debug_mode = True  # Enable for debugging
        self.alarm_points = []  # Store points with alarms
        
    def is_number(self, value):
        """Check if a value is a number (int or float)"""
        try:
            float(value.strip())
            return True
        except ValueError:
            return False
    
    def debug_print(self, message):
        """Print debug messages if debug mode is enabled"""
        if self.debug_mode:
            print(message)
    
    def has_alarms(self, object_lines):
        """Check if object has alarm links"""
        in_alarm_section = False
        alarm_lines = []
        
        for line in object_lines:
            stripped_line = line.strip()
            if stripped_line.lower() == 'alarmlinks :':
                in_alarm_section = True
                continue
            elif stripped_line.lower() == 'endalarmlinks':
                in_alarm_section = False
                break
            elif in_alarm_section:
                alarm_lines.append(stripped_line)
        
        return len(alarm_lines) > 0, alarm_lines

    def write_alarm_report(self, output_file):
        """Write alarm report to a separate file"""
        report_file = os.path.splitext(output_file)[0] + '_alarms.txt'
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("Points with Alarms Report\n")
                f.write("=" * 50 + "\n\n")
                
                for point_info in self.alarm_points:
                    f.write(f"Point Name: {point_info['name']}\n")
                    f.write(f"Point Type: {point_info['type']}\n")
                    f.write(f"Controller: {point_info.get('controller', 'Unknown')}\n")
                    f.write(f"Event Type: {point_info.get('EventType', 'Unknown')}\n")
                    f.write(f"Type Info: {point_info.get('type_info', 'Unknown')}\n")
                    f.write(f"Time Delay: {point_info.get('timeDelay', 'Unknown')}\n")
                    f.write(f"Limit: {point_info.get('Limit', 'Unknown')}\n")
                    f.write(f"Normal: {point_info.get('Normal', 'Unknown')}\n")
                    f.write(f"ACC Expression: {point_info.get('ACCExpression', 'Unknown')}\n")
                    f.write(f"Msg Text Normal: {point_info.get('MsgTextNormal', 'Unknown')}\n")
                    f.write(f"Msg Text Off Normal: {point_info.get('MsgTextOffNormal', 'Unknown')}\n")
                    f.write(f"Msg Text Fault: {point_info.get('MsgTextFault', 'Unknown')}\n")
                    f.write("Alarms:\n")
                    for alarm in point_info['alarms']:
                        f.write(f"  - {alarm}\n")
                    f.write("\n" + "-" * 50 + "\n\n")
                
            self.debug_print(f"Alarm report written to: {report_file}")
            return True
        except Exception as e:
            self.debug_print(f"Error writing alarm report: {str(e)}")
            return False

    def process_object(self, object_lines, scan_file, object_name="Unknown" ):
        """Process a single object and fix errors"""
        modified_lines = object_lines[:]
        has_format = False
        changes_made = False
        
        self.debug_print(f"\n--- Processing Object: {object_name} ---")
        
        # Check if object type is InfinitySystemVariable
        object_type = "Unknown"
        controller_name = "Unknown"
        for line in modified_lines:
            if line.strip().lower().startswith('type :'):
                object_type = line.split(':', 1)[1].strip()
                if object_type == "InfinitySystemVariable":
                    self.debug_print(f"Skipping InfinitySystemVariable type object: {object_name}")
                    return modified_lines, False
            elif line.strip().lower().startswith('controller :'):
                controller_name = line.split(':', 1)[1].strip()
            elif line.strip().lower().startswith('deviceid :'):
                # Extract controller name from DeviceId
                device_id = line.split(':', 1)[1].strip()
                controller_name = '\\'.join(device_id.split('\\')[1:])

        # Check for alarms
        has_alarms, alarm_lines = self.has_alarms(modified_lines)
        converted_names = []    
        for s in alarm_lines:
            s = s.strip()
            after_backslash = s.split("\\")[-1]
            name = after_backslash.split(" :")[0].strip()
            converted_names.append(name)

        checked_info = {}
        #Check Second File For Alarm Info
        for name in converted_names:
            checked_info = self.check_second_file(scan_file, name)
            if has_alarms:
        
             self.alarm_points.append({
            'name': object_name,
            'controller': controller_name,
            'type': object_type,
            'alarms': alarm_lines,
            'EventType': checked_info["EventType"] if checked_info else 'Unknown',
            'type_info': checked_info["type"] if checked_info else 'Unknown',
            'timeDelay': checked_info["timeDelay"] if checked_info else 'Unknown',
            'Limit': checked_info["Limit"] if checked_info else 'Unknown',
            'Normal': checked_info["Normal"] if checked_info else 'Unknown',
            'ACCExpression': checked_info["ACCExpression"] if checked_info else 'Unknown',
            'MsgTextNormal': checked_info["MsgTextNormal"] if checked_info else 'Unknown',
            'MsgTextOffNormal': checked_info["MsgTextOffNormal"] if checked_info else 'Unknown',
            'MsgTextFault': checked_info["MsgTextFault"] if checked_info else 'Unknown',
            })
        self.debug_print(f"Found alarms in point {object_name}: {len(alarm_lines)} alarms (Controller: {controller_name})")
        
        # Find all relevant lines and their indices
        value_lines = []
        tristate_lines = []
        format_line_index = -1
        
        for i, line in enumerate(modified_lines):
            stripped_line = line.strip()
            if stripped_line.lower().startswith('value :'):
                value_lines.append((i, line, stripped_line))
                self.debug_print(f"Found Value line {i}: {stripped_line}")
            elif stripped_line.lower().startswith('tristate :'):
                tristate_lines.append((i, line, stripped_line))
                self.debug_print(f"Found TriState line {i}: {stripped_line}")
            elif stripped_line.lower().startswith('format :'):
                has_format = True
                format_line_index = i
                self.debug_print(f"Found existing Format line {i}: {stripped_line}")
        
        # Process Value lines (errors 1 and 2)
        for line_index, original_line, stripped_line in value_lines:
            # Extract value part after "Value :"
            value_part = stripped_line.split(':', 1)[1].strip() if ':' in stripped_line else ""            
            self.debug_print(f"Processing Value: '{value_part}'")
            
            # Error 1: Value with On/Off should have Format : $###
            if value_part.lower() in ['on', 'off']:
                self.debug_print(f"Found On/Off value: {value_part}")
                if has_format and format_line_index >= 0:
                    # Replace existing format
                    indent = len(modified_lines[format_line_index]) - len(modified_lines[format_line_index].lstrip())
                    modified_lines[format_line_index] = ' ' * indent + 'Format : $###\n'
                    self.debug_print("Replaced existing format with $###")
                else:
                    # Add new format line after value line
                    indent = len(original_line) - len(original_line.lstrip())
                    new_format_line = ' ' * indent + 'Format : $###\n'
                    modified_lines.insert(line_index + 1, new_format_line)
                    has_format = True
                    format_line_index = line_index + 1
                    self.debug_print("Added new format line: $###")
                changes_made = True
                
            # Error 2: Value with number should have Format : ###.#
            elif self.is_number(value_part):
                self.debug_print(f"Found numeric value: {value_part}")
                if has_format and format_line_index >= 0:
                    # Replace existing format
                    indent = len(modified_lines[format_line_index]) - len(modified_lines[format_line_index].lstrip())
                    modified_lines[format_line_index] = ' ' * indent + 'Format : ###.#\n'
                    self.debug_print("Replaced existing format with ###.#")
                else:
                    # Add new format line after value line
                    indent = len(original_line) - len(original_line.lstrip())
                    new_format_line = ' ' * indent + 'Format : ###.#\n'
                    modified_lines.insert(line_index + 1, new_format_line)
                    has_format = True
                    format_line_index = line_index + 1
                    self.debug_print("Added new format line: ###.#")
                changes_made = True
            else:
                self.debug_print(f"Value '{value_part}' is text - no change needed")
        
        # Process TriState lines (error 3)
        for line_index, original_line, stripped_line in tristate_lines:
            # Extract value part after "TriState :"
            value_part = stripped_line.split(':', 1)[1].strip() if ':' in stripped_line else "" # Remove "TriState :"
            self.debug_print(f"Processing TriState: '{value_part}'")
            
            # Error 3: TriState with On/Off should have Format : $###
            if value_part.lower() in ['on', 'off']:
                self.debug_print(f"Found TriState On/Off value: {value_part}")
                if has_format and format_line_index >= 0:
                    # Replace existing format
                    indent = len(modified_lines[format_line_index]) - len(modified_lines[format_line_index].lstrip())
                    modified_lines[format_line_index] = ' ' * indent + 'Format : $###\n'
                    self.debug_print("Replaced existing format with $### for TriState")
                else:
                    # Add new format line after tristate line
                    indent = len(original_line) - len(original_line.lstrip())
                    new_format_line = ' ' * indent + 'Format : $###\n'
                    modified_lines.insert(line_index + 1, new_format_line)
                    has_format = True
                    format_line_index = line_index + 1
                    self.debug_print("Added new format line: $### for TriState")
                changes_made = True
            else:
                self.debug_print(f"TriState '{value_part}' is not On/Off - no change needed")
        
        if changes_made:
            self.debug_print(f"Object {object_name}: Changes made!")
        else:
            self.debug_print(f"Object {object_name}: No changes needed")
            
        return modified_lines, changes_made
    
    def process_file(self, input_file, output_file, scan_file):
        """Process the entire dump file"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(input_file, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        
        processed_lines = []
        current_object = []
        in_object = False
        objects_processed = 0
        errors_fixed = 0
        current_object_name = "Unknown"
        line_num = 0
        self.debug_print(f"Processing file: {input_file}")
        self.debug_print(f"Total lines in file: {len(lines)}")
        
        for line_num, line in enumerate(lines):
            stripped_line = line.strip()
            
            if stripped_line.lower().startswith('object :'):
                in_object = True
                current_object = [line]
                # Extract object name
                if len(stripped_line) > 8:  # "Object :" is 8 characters
                    current_object_name = stripped_line[8:].strip()
                else:
                    current_object_name = f"Line_{line_num}"
                self.debug_print(f"\nStarting object: {current_object_name}")
                
            elif stripped_line.lower() == 'endobject':
                if in_object:
                    current_object.append(line)
                    
                    # Process the current object
                    processed_object, changes_made = self.process_object(current_object, scan_file, current_object_name)
                    processed_lines.extend(processed_object)
                    
                    if changes_made:
                        errors_fixed += 1
                    objects_processed += 1
                    
                    current_object = []
                    in_object = False
                    current_object_name = "Unknown"
                else:
                    processed_lines.append(line)
                    
            elif in_object:
                current_object.append(line)
            else:
                processed_lines.append(line)
        
        # Write processed content to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
        
        # Write alarm report if any alarms were found
        if self.alarm_points:
            self.write_alarm_report(output_file)
        
        self.debug_print(f"\nFinal Summary:")
        self.debug_print(f"Objects processed: {objects_processed}")
        self.debug_print(f"Objects with errors fixed: {errors_fixed}")
        self.debug_print(f"Points with alarms found: {len(self.alarm_points)}")
        
        return objects_processed, errors_fixed
    
    def run(self):
        """Main execution function"""
        # Select input file
        input_file = filedialog.askopenfilename(
            title="Select Out_Alarm.txt File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Dump files", "*.dmp"),
                ("All files", "*.*")
            ]
        )
        
        if not input_file:
            messagebox.showinfo("Cancelled", "No input file selected.")
            return
        
        # Select scan file
        scan_file = filedialog.askopenfilename(
            title="Select Backup Dump File",
            filetypes=[
                ("Text files", "*.txt"),
                ("Dump files", "*.dmp"),
                ("All files", "*.*")
            ]
        )
        
        if not scan_file:
            messagebox.showinfo("Cancelled", "No scan file selected.")
            return
        # Select output file
        output_file = filedialog.asksaveasfilename(
            title="Save Fixed File As",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Dump files", "*.dmp"),
                ("All files", "*.*")
            ]
        )
        
        if not output_file:
            messagebox.showinfo("Cancelled", "No output file selected.")
            return
        
        try:
            objects_processed, errors_fixed = self.process_file(input_file, output_file, scan_file)
            
            message = (
                f"File processing completed successfully!\n\n"
                f"Objects processed: {objects_processed}\n"
                f"Objects with errors fixed: {errors_fixed}\n"
                f"Points with alarms found: {len(self.alarm_points)}\n\n"
                f"Fixed file saved as: {os.path.basename(output_file)}\n"
            )
            
            if self.alarm_points:
                message += f"\nAlarm report saved as: {os.path.basename(os.path.splitext(output_file)[0] + '_alarms.txt')}\n"
            
            messagebox.showinfo("Processing Complete", message)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while processing the file:\n\n{str(e)}"
            )

def main():
    """Main function to run the application"""
    print("Backup Dump File Error Fixer")
    print("=" * 40)
    print("\nThis script will:")
    print("1. Fix 'Value : On/Off' to have 'Format : $###'")
    print("2. Fix 'Value : <number>' to have 'Format : ###.#'") 
    print("3. Fix 'TriState : On/Off' to have 'Format : $###'")
    print("\nDebug mode is enabled - check console for detailed output.")
    print("\nStarting file selection...")
    
    fixer = DumpFileFixer()
    fixer.run()
    
    print("\nProcess completed!")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()