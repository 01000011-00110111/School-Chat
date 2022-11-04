import { User, Role, Message } from './scripts/server/mongo.js';
import Gql from './scripts/server/gql.js';
import parseRoles from './scripts/server/parseroles.js';

const clientMessage = (body, channelId) => {
  return {
    message: {
      user: {
        color: "#ffffff",
        username: "ReplyteClient",
        displayName: "Replyte Client",
        userId: 0,
        image: "/logo.svg",
        roles: [],
        userRoles: []
      },
      body: body,
      channel: channelId,
      timeCreated: Date.now(),
      first: false,
      collapse: false
    },
    _id: Math.random().toString(36).slice(2),
    channelId: channelId
  }
}

export default async function commandClient(com, io, channelId, currentUser) {
  let words = com.split` `;
  if (words[0] === "$restore") {
    const gql = new Gql(process.env.CONNECT_SID);
    let u = await User.findOne({ username: words[1] }).populate("userRoles");
    if (!u.userRoles.some(r => r.admin)) {
      let userData = await gql.raw({
        query: `query user($id: Int!) {
            user(id: $id) {
              username image displayName roles { name } isBannedFromBoards id isHacker
            }
          }`,
        variables: {
          id: u.userId
        }
      });
      if (userData?.data?.user) {
        let rls = await parseRoles(userData.data.user);
        u.userRoles = rls;
        await u.save();
        await Message.deleteMany({ user: u._id });
        io.emit("refresh", u.userId)
        io.emit("messages", clientMessage("User Restored", channelId));
      } else {
        io.emit("messages", clientMessage("Failed to restore user", channelId))
      }
    }
  }
  if (words[0] === "$assign" && currentUser.userRoles.some(x => x.name === "Owner")) {
    let u = await User.findOne({ username: words[1] }).populate("userRoles");
    let rn = words.slice(2).join` `;
    if (!u.userRoles.some(x => x.name === rn)) {
      let findRole = await Role.findOne({ name: rn });
      if (findRole) {
        u.userRoles.push(findRole);
        await u.save();
        io.emit("messages", clientMessage("Role Assigned", channelId));
        io.emit("refresh", u.userId)
      } else {
        io.emit("messages", clientMessage("Role not found", channelId));
      }
    } else {
      io.emit("messages", clientMessage("User already has that role", channelId));
    }
  }
  if (words[0] === "$demote" && currentUser.userRoles.some(x => x.name === "Owner")) {
    let u = await User.findOne({ username: words[1] }).populate("userRoles");
    let rn = words.slice(2).join` `;
    if (u.userRoles.some(x => x.name === rn)) {
      let findRole = await Role.findOne({ name: rn });
      if (findRole) {
        u.userRoles = u.userRoles.filter(x => x.name !== rn);
        
        await u.save();
        io.emit("messages", clientMessage("Role Removed", channelId));
        io.emit("refresh", u.userId);
      } else {
        io.emit("messages", clientMessage("Role not found", channelId));
      }
    } else {
      io.emit("messages", clientMessage("User doesn't have that role", channelId));
    }
  }
  if(words[0] === "$permaban"){
    let u = await User.findOne({ username: words[1] }).populate("userRoles");
    await Message.deleteMany({ user: u._id });
    u.banned = true;
    await u.save();
    io.emit("refresh", u.userId)
    io.emit("messages", clientMessage("User Perma-Banned", channelId));
  }
}