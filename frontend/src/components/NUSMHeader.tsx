import { Button } from "@/components/ui/button";
import { useGenerateSchedules } from "@/hooks/courses.hooks";


export default function NUSMHeader() {
      const { mutate: generateSchedules } = useGenerateSchedules();

    return (
        <div className="NUSMCard flex justify-between items-center">
            <div className="text-xl font-bold">Northeastern Class Schedule Generator</div>
            <div>
                <Button onClick={() => generateSchedules()}>
                    Generate Schedules
                </Button>
            </div>
        </div>
    );
}