import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}


export const stringToTimestring = (startString: string) => {
        let hrNum: number = parseInt(startString.substring(0, 2));
        let minNum: number = parseInt(startString.substring(2, 4));
        let ampm: string = "am";

        if (hrNum > 12) {
            hrNum = hrNum - 12;
            ampm = "pm";
        }

        let result: string = `${hrNum}:${minNum.toString().padStart(2, '0')}${ampm}`;
        return result;
    }


export const classColors = [
    'bg-blue-100 border-blue-400 text-blue-900 fill-blue-400',
    'bg-green-100 border-green-400 text-green-900 fill-green-400',
    'bg-orange-100 border-orange-400 text-orange-900 fill-orange-400',
    'bg-pink-100 border-pink-400 text-pink-900 fill-pink-400',
    'bg-teal-100 border-teal-400 text-teal-900 fill-teal-400',
    'bg-indigo-100 border-indigo-400 text-indigo-900 fill-indigo-400',
    'bg-red-100 border-red-400 text-red-900 fill-red-400',
    'bg-purple-100 border-purple-400 text-purple-900 fill-purple-400',
    'bg-yellow-100 border-yellow-400 text-yellow-900 fill-yellow-400',
];

export const fillColors = [
    'blue-400',
    'green-400',
    'orange-400',
    'pink-400',
    'teal-400',
    'indigo-400',
    'red-400',
    'purple-400',
    'yellow-400',
];