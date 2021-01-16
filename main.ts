import KVM from "./vm.ts"
import {data} from "./vm.ts"

export function main() {
    let i = new KVM(0xffff);
    i.load(Deno.args[0]);
    let f = i.step();
    i.printState();
    while(!f) {
        f = i.step();
        i.printState();
    }
}

main();