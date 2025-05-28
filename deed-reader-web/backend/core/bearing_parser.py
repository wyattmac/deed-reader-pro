import re
import math

class BearingParser:
    @staticmethod
    def parse_bearing(bearing_str):
        if not bearing_str:
            return None
        
        # Simple parsing for basic formats
        bearing_str = str(bearing_str).strip()
        
        # Basic pattern for North/South degrees minutes East/West
        # Support both symbol format (N45°30'E) and text format (North 45 degrees 30 minutes East)
        patterns = [
            r"(North|South|N|S)\s*(\d+)\s*degrees?\s*(\d+)?\s*minutes?.*?(East|West|E|W)",
            r"(North|South|N|S)\s*(\d+)\s*°\s*(\d+)?\s*.*?(East|West|E|W)"
        ]
        
        m = None
        for pattern in patterns:
            m = re.search(pattern, bearing_str, re.IGNORECASE)
            if m:
                break
        
        if not m:
            return None
        
        ns, deg, min_, ew = m.groups()
        deg = float(deg)
        min_ = float(min_ or 0)
        angle = deg + min_ / 60.0
        
        ns = ns[0].upper()
        ew = ew[0].upper()
        
        if ns == "N" and ew == "E":
            az = 90 - angle
        elif ns == "N" and ew == "W":
            az = 90 + angle
        elif ns == "S" and ew == "W":
            az = 270 - angle
        elif ns == "S" and ew == "E":
            az = 270 + angle
        else:
            az = 0
        
        # Normalize to 0-360 range
        while az < 0:
            az += 360
        while az >= 360:
            az -= 360
            
        return az 