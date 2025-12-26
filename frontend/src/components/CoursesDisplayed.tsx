import { useCourses } from "@/hooks/courses.hooks";
import type { MeetingTime, Section } from "@/types";
import { classColors, stringToTimestring } from "@/lib/utils";
import { Circle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Toggle } from "@/components/ui/toggle";
import { Separator } from "@/components/ui/separator";

export default function CoursesDisplay() {
  const { data } = useCourses();

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
          <Separator className="my-2" />
          <div className="flex text-lg font-bold items-center">
            <Circle
              className={`${classColors[course.colorCode]} flex-shrink-0 bg-white text-white mr-1`}
              size={20}
            />
            {course.subject}
            {course.courseNumber}: {course.courseTitle}
            <Button variant={"destructive"} className="ml-auto h-8 w-32">
              Remove Course
            </Button>
          </div>

          {course.sections.map((section) => (
            <div className="flex items-center">
              <div className="pl-7 text-[15px] mb-1.5">
                Section: {section.sequenceNumber} | {getTimeText(section)} | CRN:{" "}
                {section.courseReferenceNumber}
                <br />
                <span className="pl-4">
                  Prof: {section.faculty[0] ? section.faculty[0] : "TBD"} | Seats Left:{" "}
                  {section.seatsAvailable}/{section.maximumEnrollment}
                </span>
              </div>
              <Toggle variant={"secondary"} className="ml-auto h-8 w-32">
                Lock Section
              </Toggle>
              <Toggle variant={"secondary"} className="ml-4 h-8 w-32">
                Ignore Section
              </Toggle>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
