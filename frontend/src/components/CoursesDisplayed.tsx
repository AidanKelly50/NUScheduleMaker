import { useCourses } from "@/hooks/courses.hooks";
import type { MeetingTime, Section } from "@/types";
import { classColors, fillColors, stringToTimestring } from "@/lib/utils";
import { Circle } from "lucide-react";

export default function CoursesDisplay() {
  const { data } = useCourses();
  console.log(data);

  const getTimeText = (section: Section) => {
    let result: string = "";

    if (section.campusDescription == "Online") {
      result += "Online ";
    }

    let timesList: MeetingTime[] = section.meetingTimes;
    if (
      timesList[0].monday ||
      timesList[0].tuesday ||
      timesList[0].wednesday ||
      timesList[0].thursday ||
      timesList[0].friday
    ) {
      timesList.forEach((time) => {
        if (time.monday) {
          result += "M";
        }
        if (time.tuesday) {
          result += "T";
        }
        if (time.wednesday) {
          result += "W";
        }
        if (time.thursday) {
          result += "R";
        }
        if (time.friday) {
          result += "F";
        }

        result +=
          " " + stringToTimestring(time.beginTime) + "-" + stringToTimestring(time.endTime) + ", ";
      });
      result = result.substring(0, result.length - 2); // Remove last ", "
    } else {
      result += "Async ";
    }

    return result;
  };

  return (
    <div>
      {data?.map((course) => (
        <div>
          <div className="flex text-lg font-bold">
            <Circle
              className={`${
                classColors[course.colorCode]
              } flex-shrink-0 bg-white text-white mr-1 mb-auto mt-1`}
              size={20}
            />
            {course.subject}
            {course.courseNumber}: {course.courseTitle}
          </div>

          {course.sections.map((section) => (
            <div className="pl-7 text-[15px] mb-1.5">
              Section: {section.sequenceNumber} | {getTimeText(section)}
              <br />
              <span className="pl-4">
                CRN: {section.courseReferenceNumber} | Prof:{" "}
                {section.faculty[0] ? section.faculty[0] : "TBD"} | Seats Left:{" "}
                {section.seatsAvailable}/{section.maximumEnrollment}
              </span>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
