import { Button } from "@/components/ui/button";


export default function NUSMHeader() {
    return (
        <div className="NUSMCard flex justify-between items-center">
            <div className="text-xl font-bold">Northeastern Class Schedule Generator</div>
            <div>
                <Button>Generate Schedules</Button>
            </div>
        </div>
    );
}