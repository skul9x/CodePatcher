export namespace models {
	
	export class HistoryItem {
	    batch_id: string;
	    project_name: string;
	    project_dir: string;
	    patched_files: string[];
	    rolled_back: boolean;
	
	    static createFrom(source: any = {}) {
	        return new HistoryItem(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.batch_id = source["batch_id"];
	        this.project_name = source["project_name"];
	        this.project_dir = source["project_dir"];
	        this.patched_files = source["patched_files"];
	        this.rolled_back = source["rolled_back"];
	    }
	}

}

export namespace services {
	
	export class PatchEntry {
	    path: string;
	    content: string;
	
	    static createFrom(source: any = {}) {
	        return new PatchEntry(source);
	    }
	
	    constructor(source: any = {}) {
	        if ('string' === typeof source) source = JSON.parse(source);
	        this.path = source["path"];
	        this.content = source["content"];
	    }
	}

}

