// This component primarily constructed with Claude.

import { classColors, stringToTimestring } from "@/lib/utils";
import type { CalendarSection } from "@/types";

export default function WeeklyClassSchedule({
  classSections,
  size = "large",
}: {
  classSections: CalendarSection[];
  size: string;
}) {
  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
  const dayKeys: string[] = ["monday", "tuesday", "wednesday", "thursday", "friday"];

  // Size configurations
  const sizeConfig = {
    large: {
      timeWidth: "w-16",
      headerHeight: "h-10",
      hourHeight: 45,
      totalHeight: "495px",
      titleText: "text-xl",
      headerText: "text-base",
      timeText: "text-xs",
      classTitle: "text-sm",
      classTime: "text-xs",
      padding: "p-2",
      classPadding: "px-1.5 py-1",
      minClassHeight: "20px",
    },
    small: {
      timeWidth: "w-10",
      headerHeight: "h-6",
      hourHeight: 20,
      totalHeight: "220px",
      titleText: "text-lg",
      headerText: "text-xs",
      timeText: "text-[10px]",
      classTitle: "text-[10px]",
      classTime: "text-[9px]",
      padding: "p-2",
      classPadding: "p-0.5",
      minClassHeight: "10px",
    },
  };

  const config = size == "large" ? sizeConfig.large : sizeConfig.small;

  // Convert 24-hour time to AM/PM format
  const formatTimeAMPM = (timeStr: string, short: boolean = false): string => {
    const [hours, minutes] = timeStr.split(":").map(Number);
    const period = hours >= 12 ? "PM" : "AM";
    const displayHours = hours % 12 || 12;

    if (short && size === "small") {
      return `${displayHours}${period}`;
    }
    return `${displayHours}:${minutes.toString().padStart(2, "0")} ${period}`;
  };

  // Generate time slots from 8 AM to 6 PM
  const generateTimeSlots = (): string[] => {
    const slots: string[] = [];
    for (let hour = 8; hour <= 18; hour++) {
      slots.push(`${hour.toString().padStart(2, "0")}:00`);
    }
    return slots;
  };

  const timeSlots = generateTimeSlots();

  // Convert time string to minutes for calculations
  const timeToMinutes = (timeStr: string): number => {
    // Handle "9:15am" or "9:15pm" format
    const isPM = timeStr.toLowerCase().includes("pm");
    const isAM = timeStr.toLowerCase().includes("am");

    // Remove am/pm and parse
    const timeOnly = timeStr.toLowerCase().replace("am", "").replace("pm", "");
    const [hours, minutes] = timeOnly.split(":").map(Number);

    // Convert to 24-hour format
    let hour24 = hours;
    if (isPM && hours !== 12) {
      hour24 = hours + 12;
    } else if (isAM && hours === 12) {
      hour24 = 0; // 12am is midnight
    }

    return hour24 * 60 + minutes;
  };

  // Get position and height for a class block
  const getClassPosition = (
    beginTime: string,
    endTime: string
  ): { top: number; height: number } => {
    const startMinutes = timeToMinutes(beginTime);
    const endMinutes = timeToMinutes(endTime);
    const baseMinutes = 8 * 60; // 8 AM

    const top = ((startMinutes - baseMinutes) / 60) * config.hourHeight;
    const height = ((endMinutes - startMinutes) / 60) * config.hourHeight;

    return { top, height };
  };

  // Organize classes by day
  const getClassesByDay = (): Record<string, CalendarSection[]> => {
    const classesByDay: Record<string, CalendarSection[]> = {
      monday: [],
      tuesday: [],
      wednesday: [],
      thursday: [],
      friday: [],
    };

    classSections.forEach((section, index) => {
      const colorClass = classColors[index % classColors.length];

      section.meetingTimes.forEach((meeting) => {
        dayKeys.forEach((day) => {
          if (
            (day === "monday" && meeting.monday) ||
            (day === "tuesday" && meeting.tuesday) ||
            (day === "wednesday" && meeting.wednesday) ||
            (day === "thursday" && meeting.thursday) ||
            (day === "friday" && meeting.friday)
          ) {
            classesByDay[day].push({
              ...section,
              meetingTimes: [meeting], // ← Keep as array with single meeting
            });
          }
        });
      });
    });

    return classesByDay;
  };

  const classesByDay = getClassesByDay();

  return (
    <div className={`w-full ${config.padding} bg-white`}>
      {size === "large" && (
        <h2 className={`${config.titleText} font-bold mb-4 text-gray-800`}>
          Weekly Class Schedule
        </h2>
      )}

      <div className="flex border border-gray-300 rounded-lg overflow-hidden shadow-lg">
        {/* Time column */}
        <div className={`flex-shrink-0 ${config.timeWidth} bg-gray-50`}>
          <div
            className={`${config.headerHeight} border-b border-gray-300 flex items-center justify-center font-semibold text-gray-600 ${config.headerText}`}
          >
            {size === "large" ? "Time" : ""}
          </div>
          <div className="relative" style={{ height: config.totalHeight }}>
            {timeSlots.map((time, index) => (
              <div
                key={time}
                className={`absolute w-full border-t border-gray-200 ${config.timeText} text-gray-600 pr-1 text-right`}
                style={{ top: `${index * config.hourHeight}px` }}
              >
                {formatTimeAMPM(time, true)}
              </div>
            ))}
          </div>
        </div>

        {/* Day columns */}
        {days.map((day, dayIndex) => (
          <div key={day} className="flex-1 border-l border-gray-300">
            <div
              className={`${config.headerHeight} border-b border-gray-300 flex items-center justify-center font-semibold text-gray-700 bg-gray-50 ${config.headerText}`}
            >
              {size === "small" ? day.slice(0, 3) : day}
            </div>
            <div className="relative bg-white" style={{ height: config.totalHeight }}>
              {/* Time grid lines */}
              {timeSlots.map((time, index) => (
                <div
                  key={time}
                  className="absolute w-full border-t border-gray-100"
                  style={{ top: `${index * config.hourHeight}px` }}
                />
              ))}

              {/* Class blocks */}
              {classesByDay[dayKeys[dayIndex]].map((section, index) => {
                const { top, height } = getClassPosition(
                  stringToTimestring(section.meetingTimes[0].beginTime),
                  stringToTimestring(section.meetingTimes[0].endTime)
                );

                return (
                  <div
                    key={`${section.subject}-${section.courseNumber}-${section.sequenceNumber}-${index}`}
                    className={`absolute left-1 right-1 border-l-4 rounded ${
                      config.classPadding
                    } overflow-hidden ${classColors[section.colorCode]}`}
                    style={{
                      top: `${top}px`,
                      height: `${height}px`,
                      minHeight: config.minClassHeight,
                    }}
                  >
                    <div className={`font-semibold ${config.classTitle}`}>
                      {section.subject}
                      {section.courseNumber} - {section.sequenceNumber}
                    </div>
                    {size === "large" && (
                      <div className={config.classTime}>
                        {stringToTimestring(section.meetingTimes[0].beginTime)}&nbsp;-&nbsp;
                        {stringToTimestring(section.meetingTimes[0].endTime)}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
