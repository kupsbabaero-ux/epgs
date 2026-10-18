import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Schedule Definition
SCHEDULE = {
    "weekday": [
        ("00:00", "01:00", "Cinekwela"),
        ("01:00", "03:00", "Cinesaya"),
        ("03:00", "04:00", "Cineserye"),
        ("04:00", "06:00", "Super Sine"),
        ("06:00", "08:00", "Cinetakilya"),
        ("08:00", "10:00", "Cinekomedya"),
        ("10:00", "12:00", "Cinesaya"),
        ("12:00", "14:00", "Cineastig"),
        ("14:00", "16:00", "Cinekamao"),
        ("16:00", "18:00", "Cinetawanan"),
        ("18:00", "20:00", "Cinebarako"),
        ("20:00", "21:00", "Cineserye"),
        ("21:00", "23:00", "Cineaksyon"),
        ("23:00", "00:00", "Cinekwela"),
    ],
    "saturday": [
        ("00:00", "01:00", "Cinekwela"),
        ("01:00", "03:00", "Cinesaya"),
        ("03:00", "05:00", "Super Sine"),
        ("05:00", "07:00", "Cineuna"),
        ("07:00", "09:00", "Cinesigaw"),
        ("09:00", "11:00", "Cinekilig"),
        ("11:00", "13:00", "Cinesaya"),
        ("13:00", "15:00", "Cinematapang"),
        ("15:00", "17:00", "Cinesiga"),
        ("17:00", "19:00", "Super Sabado Sine"),
        ("19:00", "21:00", "Dolphy Hari Ng Comedy"),
        ("21:00", "23:00", "Cinematon"),
        ("23:00", "00:00", "Cinekwela"),
    ],
    "sunday": [
        ("00:00", "01:00", "Cinekwela"),
        ("01:00", "03:00", "Cinesaya"),
        ("03:00", "05:00", "Super Sine"),
        ("05:00", "07:00", "Cineuna"),
        ("07:00", "09:00", "Cinesigaw"),
        ("09:00", "11:00", "Cinekilig"),
        ("11:00", "13:00", "Cinesaya"),
        ("13:00", "15:00", "Alamat Ni Agimat"),
        ("15:00", "17:00", "Cinesiga"),
        ("17:00", "19:00", "Cinemo Box Office"),
        ("19:00", "21:00", "Markang Daboy"),
        ("21:00", "23:00", "Cinematon"),
        ("23:00", "00:00", "Cinekwela"),
    ]
}

def format_xmltv_time(date_obj, time_str):
    hours, minutes = map(int, time_str.split(":"))
    dt = date_obj.replace(hour=hours, minute=minutes, second=0)
    return dt.strftime("%Y%m%d%H%M%S +0800")

def build_epg(days_ahead=7):
    tv = ET.Element("tv", generator_info_name="Auto EPG Generator")
    
    # Channel Info
    channel = ET.SubElement(tv, "channel", id="cinemo.ph")
    display_name = ET.SubElement(channel, "display-name")
    display_name.text = "CineMo"
    
    today = datetime.datetime.now()
    
    for day_offset in range(days_ahead):
        current_date = today + datetime.timedelta(days=day_offset)
        weekday = current_date.weekday()  # 0=Monday, 5=Saturday, 6=Sunday
        
        if weekday == 5:
            day_schedule = SCHEDULE["saturday"]
        elif weekday == 6:
            day_schedule = SCHEDULE["sunday"]
        else:
            day_schedule = SCHEDULE["weekday"]
            
        for start_str, end_str, title in day_schedule:
            start_time = format_xmltv_time(current_date, start_str)
            
            # Handle overnight end time (e.g., 23:00 to 00:00 next day)
            if end_str == "00:00":
                end_date = current_date + datetime.timedelta(days=1)
                end_time = format_xmltv_time(end_date, "00:00")
            else:
                end_time = format_xmltv_time(current_date, end_str)
                
            programme = ET.SubElement(
                tv, "programme", 
                start=start_time, 
                stop=end_time, 
                channel="cinemo.ph"
            )
            prog_title = ET.SubElement(programme, "title", lang="en")
            prog_title.text = title

    xml_str = minidom.parseString(ET.tostring(tv)).toprettyxml(indent="  ")
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

if __name__ == "__main__":
    build_epg()
