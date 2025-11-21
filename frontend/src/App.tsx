import NUSMHeader from "@/components/NUSMHeader";
import { ChevronsUpDownIcon, CheckIcon } from "lucide-react";

import { Popover, PopoverTrigger, PopoverContent } from "@/components/ui/popover";
import {
  Command,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
} from "@/components/ui/command";
import { Button } from "@/components/ui/button";

import { cn } from "@/lib/utils";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { useAddCourse, useSchedules, useSemesters, useSubjects } from "@/hooks/courses.hooks";
import CoursesDisplayed from "@/components/CoursesDisplayed";
import WeeklyClassSchedule from "@/components/WeeklyClassSchedule";
import { Dialog, DialogTrigger, DialogContent } from "@/components/ui/dialog";

function App() {
  const [semesterOpen, setSemesterOpen] = useState(false);
  const [semesterValue, setSemesterValue] = useState("");

  const [subjectsOpen, setSubjectsOpen] = useState(false);
  const [subjectValue, setSubjectValue] = useState("");

  const [courseCodeValue, setCourseCodeValue] = useState("");

  const { data: semesterData } = useSemesters();
  const { data: subjectData } = useSubjects(semesterValue);

  const { mutate: addCourse } = useAddCourse();
  const { data: allScheduleData } = useSchedules();

  return (
    <div className="p-4">
      <NUSMHeader />
      <div className="grid grid-cols-2 gap-4">
        <div>
          <div className="NUSMCard">
            <div className="text-lg font-bold">Semester</div>
            <Popover open={semesterOpen} onOpenChange={setSemesterOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  aria-expanded={semesterOpen}
                  className="w-full justify-between"
                >
                  {semesterValue
                    ? semesterData?.find((semesterData) => semesterData.code === semesterValue)
                        ?.description
                    : "Select Semester"}
                  <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-full p-0">
                <Command>
                  <CommandInput placeholder="Search semesters..." />
                  <CommandList>
                    <CommandEmpty>No semester found.</CommandEmpty>
                    <CommandGroup>
                      {semesterData?.map((semesterData) => (
                        <CommandItem
                          key={semesterData.code}
                          value={semesterData.code}
                          onSelect={(currentValue) => {
                            setSemesterValue(currentValue === semesterValue ? "" : currentValue);
                            setSemesterOpen(false);
                          }}
                        >
                          <CheckIcon
                            className={cn(
                              "mr-2 h-4 w-4",
                              semesterValue === semesterData.code ? "opacity-100" : "opacity-0"
                            )}
                          />
                          {semesterData.description}
                        </CommandItem>
                      ))}
                    </CommandGroup>
                  </CommandList>
                </Command>
              </PopoverContent>
            </Popover>
          </div>

          <div className="NUSMCard">
            <div className="text-lg font-bold">Breaks</div>
            <div>Some text</div>
          </div>

          <div className="NUSMCard">
            <div className="text-lg font-bold mb-2">Courses</div>
            <div className="flex gap-4 mb-4">
              <Button
                onClick={() =>
                  addCourse({
                    semesterCode: semesterValue,
                    subjectCode: subjectValue,
                    courseCode: courseCodeValue,
                  })
                }
              >
                + Add Class
              </Button>

              <Popover open={subjectsOpen} onOpenChange={setSubjectsOpen}>
                <PopoverTrigger className="w-1/2">
                  <Button
                    variant="outline"
                    role="combobox"
                    aria-expanded={subjectsOpen}
                    className="w-full justify-between"
                  >
                    {subjectValue
                      ? subjectData?.find((subjectData) => subjectData.code === subjectValue)?.code
                      : "Select Subject"}
                    <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="p-0">
                  <Command>
                    <CommandInput placeholder="Search subjects..." />
                    <CommandList>
                      <CommandEmpty>No subject found.</CommandEmpty>
                      <CommandGroup>
                        {subjectData?.map((subjectData) => (
                          <CommandItem
                            key={subjectData.code}
                            value={subjectData.code}
                            onSelect={(currentValue) => {
                              setSubjectValue(currentValue === subjectValue ? "" : currentValue);
                              setSubjectsOpen(false);
                            }}
                          >
                            <CheckIcon
                              className={cn(
                                "mr-2 h-4 w-4",
                                subjectValue === subjectData.code ? "opacity-100" : "opacity-0"
                              )}
                            />
                            {subjectData.code}
                          </CommandItem>
                        ))}
                      </CommandGroup>
                    </CommandList>
                  </Command>
                </PopoverContent>
              </Popover>

              <Input
                className="w-1/2"
                placeholder="Class Code (0000)"
                pattern="[0-9]*"
                maxLength={4}
                onChange={(e) => setCourseCodeValue(e.target.value.replace(/\D/g, "").slice(0, 4))}
                onKeyDown={(e) => {
                  if (
                    !/[0-9]/.test(e.key) &&
                    !["Backspace", "Delete", "Tab", "ArrowLeft", "ArrowRight"].includes(e.key) &&
                    !e.ctrlKey &&
                    !e.metaKey
                  ) {
                    e.preventDefault();
                  }
                }}
              />
            </div>
            <CoursesDisplayed />
          </div>
        </div>

        <div>
          <div className="NUSMCard grid grid-cols-1">
            <div className="text-lg font-bold">
              Schedules
              <span className="text-gray-500"> ({allScheduleData?.length})</span>
            </div>
            {allScheduleData?.map((schedule, index) => (
              <Dialog key={index}>
                <DialogTrigger asChild>
                  <button className="cursor-pointer transition-opacity w-full text-left">
                    <WeeklyClassSchedule classSections={schedule.sections} size="small" />
                  </button>
                </DialogTrigger>
                <DialogContent className="!max-w-[90vw] max-h-[90vh] overflow-auto bg-white p-4">
                  <WeeklyClassSchedule classSections={schedule.sections} size="large" />
                </DialogContent>
              </Dialog>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
