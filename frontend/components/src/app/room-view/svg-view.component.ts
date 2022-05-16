import { Component, OnInit } from '@angular/core';

import { RoomDataService } from './data-services/room-data.service';
import { UserDataService } from './data-services/user-data.service';

import { ValueWatcher } from './data-services/watch';

@Component({
  selector: 'app-svg-view',
  templateUrl: './svg-view.component.html',
  styleUrls: ['./svg-view.component.scss']
})
export class RoomViewComponent implements OnInit {
  users: any[] = [];

  constructor(
    private roomDataService: RoomDataService,
    private userDataService: UserDataService
  ) {
  }

  ngOnInit(): void {
    // @ts-ignore
    let roomData = this.roomDataService.roomData;

    new ValueWatcher('roomData')
      .observable.subscribe(() => this.update());

    this.test();
  }

  test() {
    console.log(this.roomDataService.roomData)
  }

  update() {
    let roomData = this.roomDataService.roomData;

    let room = [];
    for (const userInRoom of roomData) {
      let userAsJson: any = {};

      // Add userInRoom details
      userAsJson.userInRoom = userInRoom;
      // Get user data
      this.userDataService.fetchUser(userAsJson.userInRoom.id)
        .subscribe((userData: any) => {
          let user = userData;
          delete user.password;
        })

      room.push(userAsJson);
    }

    this.users = room;
  }

}