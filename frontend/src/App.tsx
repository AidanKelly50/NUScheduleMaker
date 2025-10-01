import NUSMHeader from '@/components/NUSMHeader'
import { ChevronsUpDownIcon, CheckIcon } from 'lucide-react';

import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover';
import { Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem } from '@/components/ui/command';
import { Button } from '@/components/ui/button';

import { cn } from '@/lib/utils';
import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { useSemesters, useSubjects } from './hooks/courses.hooks';

function App() {
  const [semesterOpen, setSemesterOpen] = useState(false);
  const [semesterValue, setSemesterValue] = useState("");

  const [subjectsOpen, setSubjectsOpen] = useState(false);
  const [subjectValue, setSubjectValue] = useState("");

  const [classCodeValue, setClassCodeValue] = useState("");

  const { data: semesterData, isPending: semesterPending, error: semesterError } = useSemesters();
  const { data: subjectData, isPending: subjectPending, error: subjectError } = useSubjects(semesterValue);

  return (
    <div className='p-4'>
      <NUSMHeader />
      <div className='grid grid-cols-2 gap-4'>
        <div>
          <div className='NUSMCard'>
            <div className='text-lg font-bold'>Semester</div>
            <Popover open={semesterOpen} onOpenChange={setSemesterOpen}>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  role="combobox"
                  aria-expanded={semesterOpen}
                  className="w-full justify-between"
                >
                  {semesterValue
                    ? semesterData?.find((semesterData) => semesterData.code === semesterValue)?.description
                    : "Select Semester"}
                  <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-full p-0">
                <Command>
                  <CommandInput placeholder="Search framework..." />
                  <CommandList>
                    <CommandEmpty>No framework found.</CommandEmpty>
                    <CommandGroup>
                      {semesterData?.map((semesterData) => (
                        <CommandItem
                          key={semesterData.code}
                          value={semesterData.code}
                          onSelect={(currentValue) => {
                            setSemesterValue(currentValue === semesterValue ? "" : currentValue)
                            setSemesterOpen(false)
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

          <div className='NUSMCard'>
            <div className='text-lg font-bold'>Breaks</div>
            <div>Some text</div>
          </div>

          <div className='NUSMCard'>
            <div className='text-lg font-bold mb-2'>Courses</div>
            <div className='flex gap-4'>
              <Button className="">+ Add Class</Button>

              <Popover open={subjectsOpen} onOpenChange={setSubjectsOpen}>
                <PopoverTrigger className='w-1/2'>
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
                    <CommandInput placeholder="Search framework..." />
                    <CommandList>
                      <CommandEmpty>No framework found.</CommandEmpty>
                      <CommandGroup>
                        {subjectData?.map((subjectData) => (
                          <CommandItem
                            key={subjectData.code}
                            value={subjectData.code}
                            onSelect={(currentValue) => {
                              setSubjectValue(currentValue === subjectValue ? "" : currentValue)
                              setSubjectsOpen(false)
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
                onChange={(e) => setClassCodeValue(e.target.value.replace(/\D/g, '').slice(0, 4))}
                onKeyDown={(e) => {
                  if (!/[0-9]/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight'].includes(e.key) && !e.ctrlKey && !e.metaKey) {
                    e.preventDefault();
                  }
                }}
              />
            </div>
          </div>
        </div>
        
        <div>
          <div className='NUSMCard'>Hi2</div>
        </div>

      </div>
    </div>
  )
}

export default App;
