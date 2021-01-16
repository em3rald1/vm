//import {} from 'https://deno.land/std@1.0.5/mod.ts';
export function read(fileName: string | URL) : Uint8Array {
    return Deno.readFileSync(fileName);
}

export const data: Map<string, number> = new Map<string, number>();
data.set('lda', 0x0a);
data.set('ldx', 0x0b);
data.set('ldy', 0x0c);

data.set('sta', 0x0d);
data.set('stx', 0x0e);
data.set('sty', 0x0f);

data.set('psha', 0x10);
data.set('pshx', 0x11);
data.set('pshy', 0x12);

data.set('popa', 0x13);
data.set('popx', 0x14);
data.set('popy', 0x15);

data.set('cmp', 0x16);
data.set('beq', 0x17);
data.set('bne', 0x18);

data.set('call', 0x19);
data.set('calr', 0x1a);
data.set('calm', 0x1b);

data.set('ret', 0x1c);
data.set('cmt', 0xfe);
data.set('hlt', 0xff);

data.set('nop', 0x1);


/*export const data = {
    "lda": 0x0a,
    'ldx': 0x0b,
    'ldy': 0x0c,

    'sta': 0x0d,
    'stx': 0x0e,
    'sty': 0x0f,

    'psha': 0x10,
    'pshx': 0x11,
    'pshy': 0x12,

    'popa': 0x13,
    popx: 0x14,
    popy: 0x15,

    cmp: 0x16,
    beq: 0x17,
    bne: 0x18,

    call: 0x19,
    calr: 0x1a,
    calm: 0x1b,
    ret: 0x1c,
    comment: 0xfe,
    hlt: 0xff,
}
*/
export default class KVM {
    acc: number = 0;
    x: number = 0;
    y: number = 0;
    ip: number = 0;
    sp: number = 0;
    zero: boolean = true;
    start_addr: number = 0;
    
    memory: Uint8Array;
    constructor(size_t: number) {
        this.memory = new Uint8Array(size_t);
        this.sp = 0x3fff;
    }
    fetch() {
        return this.memory[this.ip++];
    }
    push(data: number) {
        this.memory[this.sp] = data;
        this.sp--;
    }
    pop() {
        this.sp++;
        return this.memory[this.sp];
    }
    step() {
        let r : boolean = false;
        let instr : number = this.fetch();
        switch(instr) {
            case data.get('lda'): {
                let arg = this.fetch();
                this.acc = arg;
                break;
            }
            case data.get('ldx'): {
                let arg = this.fetch();
                this.x = arg;
                break;
            }
            case data.get('ldy'): {
                this.y = this.fetch();
                break;
            }
            case data.get('sta'): {
                this.memory[this.fetch()] = this.acc;
                break;
            }
            case data.get('stx'): {
                this.memory[this.fetch()] = this.x;
                break;
            }
            case data.get('sty'): {
                this.memory[this.fetch()] = this.y;
                break;
            }
            case data.get('psha'): {
                this.push(this.acc);
                break;
            }
            case data.get('pshx'): {
                this.push(this.x);
                break;
            }
            case data.get('pshy'): {
                this.push(this.y);
                break;
            }
            case data.get('popa'): {
                this.acc = this.pop();
                break;
            }
            case data.get('popx'): {
                this.x = this.pop();
                break;
            }
            case data.get('popy'): {
                this.y = this.pop();
                break;
            }
            case data.get('cmp'): {
                let d1 = this.fetch();
                let d2 = this.fetch();
                let r = d1-d2;
                this.zero = (r == 0);
                break;
            }
            case data.get('beq'): {
                let d1 = this.fetch();
                let d2 = this.fetch();
                let addr = (d1 << 8) | d2;
                this.start_addr = this.ip;
                if(this.zero) {
                    this.ip = addr;
                }
                //0b00110101;
                break;
            }
            case data.get("bne"): {
                let d1 = this.fetch();
                let d2 = this.fetch();
                let addr = (d1 << 8) | d2;
                this.start_addr = this.ip;
                if(!this.zero) {
                    this.ip = addr;
                }
                break;
            }
            case data.get('call'): {
                let d1 = this.fetch();
                let d2 = this.fetch();
                let addr = (d1 << 8) | d2;
                this.start_addr = this.ip;
                this.ip = addr;
                break;
            }
            case data.get('ret'): {
                this.ip = this.start_addr;
                break;
            }
            case data.get('cmt'): {
                let data = this.fetch();
                for(let i = 0; i < data; i++) {
                    this.fetch();
                }
                break;
            }
            case data.get('hlt'): {
                r = true;
            }
        }
        return r;
    }
    load(data: string | Uint8Array) : void {
        let data_ : Uint8Array;
        if(typeof data == 'string') {
            data_ = read(data);
        } else data_ = data;
        for(let i = 0; i < data_.length; i++) {
            this.memory[i] = data_[i];
        }
    }
    printState() {
        console.log(`A: ${this.acc}\n` +
                    `X: ${this.x}\n`+
                    `Y: ${this.y}\n`+
                    `IP: ${this.ip}\n`+
                    `SP: ${this.sp}\n`
        );
    }
}